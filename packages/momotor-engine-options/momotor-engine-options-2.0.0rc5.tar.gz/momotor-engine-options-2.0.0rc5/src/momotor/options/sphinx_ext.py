""" Sphinx extension for documenting checklet option definitions. """
from __future__ import annotations

import textwrap
import typing

from momotor.bundles.elements.options import Option
from momotor.options import OptionDefinition, OptionNameDomain

try:
    from docutils import nodes
    from docutils.nodes import make_id
    from docutils.parsers.rst import Directive, directives
    from docutils.parsers.rst.states import RSTState
    from docutils.statemachine import ViewList, StringList

    from sphinx import addnodes
    from sphinx.addnodes import desc_signature
    from sphinx.application import Sphinx
    from sphinx.directives import ObjectDescription
    from sphinx.domains import Domain, ObjType, Index
    from sphinx.domains.python import PyXRefRole, PyVariable
    from sphinx.domains.std import StandardDomain
    from sphinx.errors import ExtensionError
    from sphinx.ext.autodoc import Documenter, AttributeDocumenter, DataDocumenter
    from sphinx.roles import XRefRole
    from sphinx.util import import_object, nested_parse_with_titles, logging
    from sphinx.util.docfields import Field
    from sphinx.util.docstrings import prepare_docstring
    from sphinx.util.nodes import make_refnode
    from sphinx.util.typing import OptionSpec

except ImportError:
    has_sphinx = False
else:
    has_sphinx = True

if has_sphinx:
    logger = logging.getLogger(__name__)

    def document_option_definition(
            option: OptionDefinition, tab_width: int = 8, *,
            module: str | None = None,
            checklet: str | None = None,
            step: str | None = None,
            no_index_entry: bool = False,
            no_contents_entry: bool = False,
    ) -> typing.Generator[str, None, None]:
        """ Generate a reStructuredText description for the given option definition.

        :param option: The option definition to document.
        :param tab_width: The tab width to use for indentation.
        :param no_index_entry: Whether to suppress the index entry for this option.
        :param no_contents_entry: Whether to suppress the contents entry for this option.
        :param module: The module name to use for the option.
        :param checklet: The checklet name to use for the option.
        :param step: The step name to use for the option.
        :return: A generator yielding the lines of the reStructuredText description.
        """
        name = option.name
        if (domain := option.domain) != Option.DEFAULT_DOMAIN:
            name = f'{name}@{domain}'

        yield f'.. momotor:option:: {name}'

        if module:
            yield f'   :module: {module}'
        if checklet:
            yield f'   :checklet: {checklet}'
        if step:
            yield f'   :step: {step}'
        if no_index_entry:
            yield '   :no-index-entry:'
        if no_contents_entry:
            yield '   :no-contents-entry:'

        if option.deprecated:
            if isinstance(option.deprecated, str):
                prefix = '   :deprecated: '
                for line in prepare_docstring(option.deprecated, tab_width):
                    yield prefix + line
                    prefix = '                '
            else:
                yield '   :deprecated:'
                yield ''
        else:
            yield ''

        if option.doc is not None:
            for line in prepare_docstring(option.doc, tab_width):
                yield f'   {line}'

        yield f'   :type: {"*Any*" if option.type is None else option.type}'
        yield f'   :required: *{option.required!r}*'
        yield f'   :multiple: *{option.multiple!r}*'
        yield f'   :all: *{option.all!r}*'
        yield f'   :location: {", ".join(option.location)}'

        default = option.default
        if default is option.NO_DEFAULT:
            yield f'   :default: *No default*'
        elif option.type in {'bool', 'boolean'}:
            yield f'   :default: *{default!r}*'
        else:
            yield f'   :default: {default!r}'

        yield ''

    def parse_rst(rst: str, state: RSTState) -> list[nodes.Node]:
        vl = ViewList(textwrap.dedent(rst).splitlines(), source='')
        node = nodes.paragraph()
        # noinspection PyTypeChecker
        nested_parse_with_titles(state, vl, node)

        return [node]

    def option_deprecation_note(state: RSTState, note: str | None = None) -> list[nodes.Node]:
        if not note:
            note = 'This option is deprecated.'

        note_nodes = parse_rst(textwrap.dedent(note), state=state)

        return [
            nodes.admonition(
                '',
                nodes.title(
                    '',
                    'Deprecated'
                ),
                *note_nodes,
                classes=['attention']
            )
        ]

    class OptionField(Field):
        pass

    class CheckletOptionDirective(ObjectDescription[str]):
        option_spec: OptionSpec = {
            **ObjectDescription.option_spec,
            'deprecated': directives.unchanged,
            'module': directives.unchanged,
            'checklet': directives.unchanged,
            'step': directives.unchanged,
        }

        doc_field_types = [
            OptionField('type', label='Type', names=('type',), has_arg=False),
            OptionField('required', label='Required', names=('required',), has_arg=False),
            OptionField('multiple', label='Multiple', names=('multiple',), has_arg=False),
            OptionField('all', label='All', names=('all',), has_arg=False),
            OptionField('location', label='Location', names=('location',), has_arg=False),
            OptionField('default', label='Default', names=('default',), has_arg=False),
        ]

        def handle_signature(self, sig: str, signode: desc_signature) -> str:
            module = self.options.get('module', self.env.ref_context.get('py:module'))
            checklet = self.options.get('checklet', self.env.ref_context.get('py:class'))
            step = self.options.get('step')

            if step:
                fullname = f'{step}.{sig}'
                node_id = make_id(fullname)
            elif checklet:
                fullname = f'{checklet}.{sig}'
                if module:
                    node_id = make_id(f'{module}.{checklet}._meta.options.{sig}')
                else:
                    node_id = make_id(f'{checklet}._meta.options.{sig}')
            else:
                fullname = sig
                node_id = make_id(fullname)

            signode['module'] = module
            signode['checklet'] = checklet
            signode['fullname'] = fullname
            signode['name'] = sig
            signode['ids'].append(node_id)

            option_name = OptionNameDomain.from_qualified_name(sig)

            signode += addnodes.desc_name(option_name.name, option_name.name)

            if option_name.domain != Option.DEFAULT_DOMAIN:
                nodetext = f'@{option_name.domain}'
                signode += addnodes.desc_addname(nodetext, nodetext)

            signode += addnodes.desc_annotation(' option', ' option')

            return fullname

        def get_index_text(self, sig: str) -> str:
            step = self.options.get('step')
            if step:
                return f'{sig} (option of {step})'

            checklet = self.options.get('checklet')
            if checklet is None:
                module = self.env.ref_context.get('py:module')
                classname = self.env.ref_context.get('py:class')
                if module and classname:
                    checklet = f'{module}.{classname}'
                elif classname:
                    checklet = classname

            if checklet:
                return f'{sig} ({checklet} option)'

            return f'{sig} (option)'

        def add_target_and_index(self, name: str, sig: str, signode: desc_signature) -> None:
            super().add_target_and_index(name, sig, signode)
            node_id = signode['ids'][0]

            domain = typing.cast(MomotorDomain, self.env.get_domain('momotor'))
            domain.note_ref('option', name, sig)

            if 'no-index-entry' not in self.options:
                index_text = self.get_index_text(sig)

                self.indexnode['entries'].append(
                    # (entrytype, entryname, target, ignored, key)
                    ('single', index_text, node_id, '', None),
                )

        def transform_content(self, contentnode: addnodes.desc_content) -> None:
            if 'deprecated' in self.options:
                contentnode[0:0] = option_deprecation_note(self.state, self.options.get('deprecated'))

        def _object_hierarchy_parts(self, sig_node: desc_signature) -> tuple[str, ...]:
            if 'name' not in sig_node:
                return ()

            name = sig_node['name']

            if step := sig_node.get('step'):
                return (*step.split('.'), name)  # noqa

            parts = (name,)
            if checklet := sig_node.get('checklet'):
                parts = (checklet, *parts)
            if modname := sig_node.get('module'):
                parts = (modname, *parts)

            return parts

        def _toc_entry_name(self, sig_node: desc_signature) -> str:
            if not sig_node.get('_toc_parts'):
                return ''

            config = self.env.app.config
            *parents, name = sig_node['_toc_parts']
            if config.toc_object_entries_show_parents == 'domain':
                return sig_node.get('fullname', name) + ' option'
            if config.toc_object_entries_show_parents == 'hide':
                return name + ' option'
            if config.toc_object_entries_show_parents == 'all':
                return '.'.join(parents + [name]) + ' option'
            return ''


    class OptionDefinitionVariableDirective(PyVariable):
        pass

    class MomotorDomain(Domain):
        name = 'momotor'
        label = 'Momotor'

        object_types: dict[str, ObjType] = {
            'option': ObjType('option', 'option'),
            'optiondefvar': ObjType('optiondef', 'optiondef'),
        }

        directives = {
            'option': CheckletOptionDirective,
            'optiondefvar': OptionDefinitionVariableDirective,
        }

        roles = {
            'option': XRefRole(),
        }

        initial_data = {
            'options': []
        }

        # def get_full_qualified_name(self, node: nodes.Element) -> str | None:
        #     return f'option.{node.arguments[0]}'

        def get_objects(self):
            yield from self.data['options']

        def resolve_xref(self, env, fromdocname, builder, typ, target, node, contnode) -> nodes.reference | None:
            for name, sig, typ, todocname, anchor, prio in self.get_objects():
                if sig == target:
                    return make_refnode(builder, fromdocname, todocname, anchor, contnode, sig)

            return None

        def note_ref(self, typ: str, name: str, sig: str) -> str:
            anchor = make_id(name)

            self.data[f'{typ}s'].append(
                # name, dispname, type, docname, anchor, priority
                (name, sig, typ, self.env.docname, anchor, 0)
            )

            return anchor

    class OptionDefinitionVariableDocumenter(DataDocumenter):
        objtype = 'optiondefvar'
        domain = 'momotor'

        @classmethod
        def can_document_member(
                cls,
                member: typing.Any, membername: str, isattr: bool, parent: typing.Any
        ) -> bool:
            return isinstance(member, OptionDefinition) and isattr

        def should_suppress_value_header(self) -> bool:
            return True

        def add_content(self, more_content: StringList | None) -> None:
            super().add_content(more_content)

            sourcename = self.get_sourcename()
            tab_width = self.directive.state.document.settings.tab_width

            for line in document_option_definition(self.object, tab_width):
                self.add_line(line, sourcename)


    def setup(app: Sphinx) -> dict[str, typing.Any]:
        from importlib.metadata import version

        app.setup_extension('sphinx.ext.autodoc')
        app.add_autodocumenter(OptionDefinitionVariableDocumenter)
        app.add_domain(MomotorDomain)

        return {
            'version': version('momotor-engine-options'),
            'parallel_read_safe': True,
            'parallel_write_safe': True,
        }
