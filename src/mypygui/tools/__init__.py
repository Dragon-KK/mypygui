def validate_text_input(event, span, clipboard, validation_function = lambda e:'hover' in e.state):

    if not validation_function(span):return
    if event.info._e.char == '':
        return
    o = ord(event.info._e.char)

    if o == 8:
        span.content = span.content[:-1]
    elif o == 22:
        txt = clipboard.get()
        span.content += txt
    elif o == 3:
        clipboard.set(span.content)
    else:
        span.content += event.info._e.char
    span.render_node.request_reflow()