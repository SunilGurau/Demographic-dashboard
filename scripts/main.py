from dropdown import extract_dropdown_element

if __name__ == "__main__":
    # Get the outer HTML content of the desired element
    # start_time = time.time()
    URL = "https://censusnepal.cbs.gov.np/results/population"
    asyncio.run(extract_dropdown_element(URL))
    # end_time = time.time()
    # print("Execution time:", end_time - start_time, "seconds")