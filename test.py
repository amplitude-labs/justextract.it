from env import setup_secrets
from objects.PDFFile import PDFFile
from objects.filters.ContentTypeFilter import ContentTypeFilter
from objects.filters.KeywordFilter import KeywordFilter
from objects.filters.PageNumberFilter import PageNumberFilter
from objects.filters.PageOrientationFilter import PageOrientationFilter

setup_secrets()

file = PDFFile("Recitation+04.pdf")
print(file.document.page_count)
file.filter_by_page_number(PageNumberFilter(
    pages=[1, 2, 3, 4, 5], include=True))
file.filter_by_page_orientation(PageOrientationFilter(
    orientation="portrait", include=True))
print(file.get_nodes())
print(file.document.page_count)
