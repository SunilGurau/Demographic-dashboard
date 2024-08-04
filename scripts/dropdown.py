import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import time
import pandas as pd
from dataclasses import dataclass
from enum import Enum

from utils import *
from selector import *

class SelectBy(Enum):
    PROVINCE = 1
    DISTRICT = 2

@dataclass
class District:
    district: str
    province: str
    population: int
    male_population: int
    female_population: int
    sex_ratio: float
    population_density: float
    annual_pgr: float

async def get_dropdown_html(page, selectby = SelectBy.PROVINCE):
    '''Returns the HTML content of for dropdowns in the page'''

    dropdown_button_selector = province_dropdown_button_selector
    dropdown_selector = province_dropdown_selector

    if selectby == SelectBy.DISTRICT:
        dropdown_button_selector = district_dropdown_button_selector
        dropdown_selector = district_dropdown_selector

    await page.waitForSelector(dropdown_button_selector)
    await page.click(dropdown_button_selector)

    await page.waitForSelector(dropdown_selector)
    dropdown_html_content = await get_html_content(page, dropdown_selector)

    await page.click(dropdown_button_selector)#to remove drop down

    return dropdown_html_content

# async def get_province_data(browser, province_selector):
#     page = await browser.newPage()
#     await page.goto(URL)
#     await page.click(province_dropdown_button_selector)
#     await page.click(province_selector)
#     await asyncio.sleep(0.5)

#     population_html_content = await get_html_content(page, total_population_selector)

#     population_soup = BeautifulSoup(population_html_content, 'html.parser')
#     # print(population_soup.text)

#     await page.close()


async def extract_dropdown_element(url):
    # Launch the browser
    browser = await launch(headless = True)  # Set headless=True for a headless browser
    
    # Create a new page
    page = await browser.newPage()
    
    # Navigate to the URL
    await page.goto(URL)

    province_dropdown_html_content = await get_dropdown_html(page, selectby = SelectBy.PROVINCE)
    # provinces = get_dropdown_options(province_dropdown_html_content)

    provinces_soup = BeautifulSoup(province_dropdown_html_content, 'html.parser')
    province_tags = provinces_soup.find(recursive=False).find(recursive=False).find_all(recursive = False)[1:]  # Set recursive=False to find only immediate children

    # print(province_tags)

    df = pd.DataFrame(columns = ["district", "province", "population", "male_population", "female_population", "sex_ratio", "population_density", "annual_pgr"])
    for province_tag in province_tags:
        await page.waitForSelector(province_dropdown_button_selector)
        await page.click(province_dropdown_button_selector)
        await page.waitForSelector(province_dropdown_selector)
        
        province_selector = bs4tag_to_css_selector(province_tag)
        await page.click(province_selector)

        # await asyncio.sleep(1)

        district_dropdown_html_content = await get_dropdown_html(page, selectby= SelectBy.DISTRICT)
        districts_soup = BeautifulSoup(district_dropdown_html_content, 'html.parser')
        district_tags = districts_soup.find(recursive=False).find(recursive=False).find_all(recursive = False)[1:]

        for district_tag in district_tags:
            await page.waitForSelector(district_dropdown_button_selector)
            await page.click(district_dropdown_button_selector)
            await page.waitForSelector(district_dropdown_selector)
            
            district_selector = bs4tag_to_css_selector(district_tag)
            await page.click(district_selector)
            await asyncio.sleep(0.7)

            district = district_tag.get_text().strip()
            province = province_tag.get_text().strip()
            population = await selector_to_text(page, total_population_selector)

            genderwise_population_dict = await get_genderwise_population(page, genderwise_population_xpath)
            male_population = genderwise_population_dict['male']
            female_population = genderwise_population_dict['female']

            population_density = await selector_to_text(page, population_density_selector)
            annual_pgr = await selector_to_text(page, annual_pgr_selector)
            sex_ratio = await selector_to_text(page, sex_ratio_selector)

            

            record = District(
                district = district,
                province = province,
                population = population,
                male_population = male_population,
                female_population = female_population,
                sex_ratio = sex_ratio,
                population_density = population_density,
                annual_pgr = annual_pgr
            ).__dict__
    
            # print(record)
            df.loc[len(df)] = record

        
    df.to_csv('district.csv')




    # option_selectors = list(map(tag_to_css_selector, option_tags))
    # # Print the nested tags
    # # for i in option_selectors:
    # #     print(i)
    # coro_list = []
    # for option_selector in option_selectors:
    #     coro_list.append(get_province_data(browser, option_selector))

    # await asyncio.gather(*coro_list)
        


    # Close the browser
    await page.close()
    await browser.close()
