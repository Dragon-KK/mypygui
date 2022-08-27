import mypygui
import mypygui.parsers.css_parser
import mypygui.util.json as json
xs = mypygui.parsers.css_parser.parse_sheet_from_raw(
    mypygui.fs.load(mypygui.fs.URI.from_local_path_string(__file__).parent.join('mypygui', 'page', 'objects', 'cssom', '__default.css'))
)

print(xs.selectors)