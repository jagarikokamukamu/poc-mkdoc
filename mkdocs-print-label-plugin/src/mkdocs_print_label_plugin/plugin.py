import base64
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options

class PrintLabelPlugin(BasePlugin):
    config_scheme = (
        ('label_type', config_options.Type(str, default='none')),
    )

    def on_config(self, config):
        svg_shagaihi = '<svg width="80" height="30" xmlns="http://www.w3.org/2000/svg"><rect x="2" y="2" width="76" height="26" fill="white" stroke="red" stroke-width="2"/><text x="40" y="20" font-family="sans-serif" font-size="14" fill="red" text-anchor="middle" font-weight="bold">社外秘</text></svg>'

        svg_hi = '<svg width="40" height="40" xmlns="http://www.w3.org/2000/svg"><rect x="2" y="2" width="36" height="36" fill="white" stroke="red" stroke-width="2"/><text x="20" y="26" font-family="sans-serif" font-size="18" fill="red" text-anchor="middle" font-weight="bold">秘</text></svg>'

        svgs = {
            'shagaihi': svg_shagaihi,
            'hi': svg_hi
        }
        
        label = self.config.get('label_type')
        if label in svgs:
            b64_svg = base64.b64encode(svgs[label].encode('utf-8')).decode('utf-8')
            # 印刷時のみ適用されるCSS
            self.custom_css = f"""
            <style>
            @media print {{
                @page {{
                    @top-right {{
                        content:url("data:image/svg+xml;base64,{b64_svg}");
                        vertical-align: middle;
                    }}

            }}
            }}
            </style>
            """
        else:
            self.custom_css = ""
        return config

    def on_post_page(self, output, page, config):
        if self.custom_css:
            return output.replace("</head>", f"{self.custom_css}</head>")
        return output
