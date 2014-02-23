from scrapy.item import Item, Field

class ApkItem(Item):

    # App name, developer, and genre
    name = Field()
    developer = Field()
    genre = Field()

    # User rating
    score = Field()

    # Additional information
    date_published = Field()
    file_size = Field()
    num_downloads = Field()
    software_version = Field()
    operating_systems = Field()

    # Where the APK file came from
    download_url = Field()

    # For Files Pipeline
    file_urls = Field()
    files = Field()