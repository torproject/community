sortby_resources_ini = \
'''[model]
name = Community Resources
label = {{ this.title }}
inherits = page

[fields.sortby_resources]
label = Sortby resources
type = text

[fields.sortby_resources_visible]
label = Visible sortby resources
type = strings

[fields.current_topic]
label = Current topic filter
type = text

[fields.current_lang]
label = Current language filter
type = text

[fields.current_lang_code]
label = Current language filter ISO code
type = text

[fields.current_author]
label = Current author filter
type = text
'''

contents_lr_tmpl = \
'''section: {section}
---
_model: sortby_resources
---
section_id: {section_id}
---
color: {color}
---
_template: {template}
---
title: {title}
---
subtitle: {subtitle}
---
cta: {cta}
---
html: {html}
---
sortby_resources: {sortby_resources}
---
sortby_resources_visible: {sortby_resources_visible}
---
current_topic: {current_topic}
---
current_lang: {current_lang}
---
current_lang_code: {current_lang_code}
---
current_author: {current_author}
---
body:

{body}
'''
