from bs4 import BeautifulSoup
import asyncio

selector_in_JS = lambda x: x.replace('\\', '\\\\')
id_to_css_selector = lambda id: ('#' + id.replace(':', '\\:'))
bs4tag_to_css_selector = lambda tag: id_to_css_selector(tag.get('id'))

async def get_html_content(page, selector):
    dropdown_selector_JS = selector_in_JS(selector)
    dropdown_html_content = await page.evaluate(f'document.querySelector("{dropdown_selector_JS}").outerHTML')
    return dropdown_html_content

async def selector_to_text(page, selector):
    html_content = await get_html_content(page, selector)
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text().strip()
    return text

async def get_genderwise_population(page, tooltip_xpath):
    await asyncio.sleep(1)
    bounding_element = await page.waitForXPath('/html/body/div[1]/div/main/main/div/div/div[2]/div/div[1]/section/div[2]/div[1]/div[3]/div/div/div/div')
    bounding_element_html = await page.evaluate('(element) => element.outerHTML', bounding_element)
    
    bounding_element_soup = BeautifulSoup(bounding_element_html, 'html.parser')

    bars = bounding_element_soup.find_all(class_ = 'apexcharts-bar-area')

    population_list = list()
    population_dict = dict()

    print(len(bars))
    for bar in bars:
        bar_selector = bs4tag_to_css_selector(bar)

        await page.waitForSelector(bar_selector)

        while True:
            try:
                await page.hover(bar_selector)
                break
            except:
                pass
        
        await asyncio.sleep(0.1)#the website uses same tooltip to display both the male and female population; so allow time to update render after hover
        tooltip = await page.waitForXPath(tooltip_xpath)
        tooltip_html = await page.evaluate('(element) => element.outerHTML', tooltip)

        tooltip_soup = BeautifulSoup(tooltip_html, 'html.parser')
        population = tooltip_soup.get_text().split()[0]
        population_list.append(population)

    population_dict['male'] = population_list[0]
    population_dict['female'] = population_list[1]
    
    return population_dict