if False:from ..src.mypygui.page.scripts.script_globals import *
elems = document.get_elements_by_tag_name('img')
xs = document.get_elements_by_class_name('img-container')[0]
# xs.event_emitter.subscribe(Event.Types.hover_start,lambda e: print(xs.state))
def on_click(e):
    return reload_page()
    redirect(document.root_directory._uri.make("./index.html"))
    # e.target.remove()
    # if len(xs.children) == 0:
    #     xs.remove()
    #     try:
    #         document.get_elements_by_tag_name('body')[0].append_child(
    #             DOMNode(
    #                 class_list = ClassList(('img-container',)),
    #                 tag = 'div',
    #                 children=[
    #                     DOMNode(
    #                         tag = 'img',
    #                         image = resource_handler.request_resource(
    #                             uri = document.root_directory._uri.make("https://picsum.photos/900"),
    #                             file_type = FileType.bytes,
    #                             data_resolver = Image.handle_resource_request
    #                         )
    #                     ),
    #                     DOMNode(
    #                         tag = 'img',
    #                         image = resource_handler.request_resource(
    #                             uri = document.root_directory._uri.make("https://picsum.photos/1200"),
    #                             file_type = FileType.bytes,
    #                             data_resolver = Image.handle_resource_request
    #                         )
    #                     ),
    #                     DOMNode(
    #                         tag = 'img',
    #                         image = resource_handler.request_resource(
    #                             uri = document.root_directory._uri.make("https://picsum.photos/300"),
    #                             file_type = FileType.bytes,
    #                             data_resolver = Image.handle_resource_request
    #                         )
    #                     ),
    #                     DOMNode(
    #                         tag = 'img',
    #                         image = resource_handler.request_resource(
    #                             uri = document.root_directory._uri.make("https://picsum.photos/400"),
    #                             file_type = FileType.bytes,
    #                             data_resolver = Image.handle_resource_request
    #                         )
    #                     )
    #                 ]
    #             )
    #         )
    #     except Exception as e:
    #         print(e)
    #     console.debug('Changes have been made to dom')

def handle(elem):
    elem.event_emitter.subscribe(Event.Types.click, on_click)

for elem in elems:
    handle(elem)



