
# :: Handles conversion of html data into an image

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def render_bracket(html_path: str, imgs_dir: str, unique_id: str) -> None:
    # Set up headless Firefox
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    # Load the HTML file
    driver.get(f'file://{html_path}')

    # Set the window size to capture the full page (adjust width if needed)
    driver.set_window_size(975, 825)  # w / h

    # Take a screenshot and save it
    driver.save_screenshot(f'{imgs_dir}/bracket_e{unique_id}.png')

    # Close the browser
    driver.quit()
