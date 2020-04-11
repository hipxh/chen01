from poium import PageElement,Page,PageElements

class chooseClassPage(Page):
    # elem_id = PageElement(id_='id')
    # elem_name = PageElement(name_='name')
    # elem_class = PageElement(class_name='class')
    # elem_tag = PageElement(tag='input')
    # elem_link_text = PageElement(link_text='this is link')
    # elem_partial_link_text = PageElement(partial_link_text='is link')
    # elem_css = PageElement(css='#id')
    btns_enter_answer = PageElements(xpath='//button[@class="btn bg-primary"]')
