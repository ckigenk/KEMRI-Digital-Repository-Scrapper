from bot.scrapper import Thesis
from bot.constants import URL


__author__="Collins Kigen"
__copyright__="Copyright 2025"
__credits__=["Collins Kigen"]
__license__="GPL"
__version__="1.0.0"
__maintainer__="Collins Kigen"
__email__="ckigen.k@gmail.com"

inst=Thesis()
inst.land_site_page()
inst.scrape_thesis()
inst.save_data()