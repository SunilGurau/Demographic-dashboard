province_dropdown_button_selector = "#__next > div > main > main > div > div > div.select-field > div:nth-child(1) > div > div > div.select__value-container.select__value-container--has-value.css-hlgwow"
province_dropdown_selector = r"#react-select-\:Rmkqm\:-listbox"
district_dropdown_button_selector = "#__next > div > main > main > div > div > div.select-field > div:nth-child(2) > div > div > div.select__value-container.select__value-container--has-value.css-hlgwow"
district_dropdown_selector = r"#react-select-\:R16kqm\:-listbox"


#selectors used for pypeteers can have '\' symbol all by itself, escaping the symbol works fine too.
#selectors used in JS need to have it escaped, so '\\' is replaced by '\\\\'
total_population_selector = "#__next > div > main > main > div > div > div:nth-child(2) > div > div.grid > section > div.grid.gap-1.sm\:grid-cols-2.flex-1 > div:nth-child(1) > div.flex.gap-0\.5.items-center > h3"
genderwise_population_xpath = "/html/body/div[1]/div/main/main/div/div/div[2]/div/div[1]/section/div[2]/div[1]/div[3]/div/div/div/div/div[2]/div/div[2]"
population_density_selector = "#__next > div > main > main > div > div > div:nth-child(2) > div > div.grid > section > div.grid.gap-1.sm\:grid-cols-2.flex-1 > div:nth-child(3) > div.flex.gap-0\.5.items-center > h3"
annual_pgr_selector = "#__next > div > main > main > div > div > div:nth-child(2) > div > div.grid > section > div.grid.gap-1.sm\:grid-cols-2.flex-1 > div:nth-child(4) > div.flex.gap-0\.5.items-center > h3"
sex_ratio_selector = "#__next > div > main > main > div > div > div:nth-child(2) > div > div.grid > section > div.grid.gap-1.sm\:grid-cols-2.flex-1 > div:nth-child(2) > div.flex.gap-0\.5.items-center > h3"
