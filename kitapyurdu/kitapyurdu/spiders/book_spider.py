from scrapy import Spider, Request

class BooksSpider(Spider):
    name = "books"
    start_urls = [
        "https://www.kitapyurdu.com/index.php?route=product/bargain&sort=publish_date&order=DESC&discount=60&filter_in_stock=1"
    ]
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 6  
    }

    def parse(self, response):
        book_names = response.css("div.name.ellipsis a span::text").extract()
        book_authors = response.css("div.author span a span::text").extract()
        book_publishers = response.css("div.publisher span a span::text").extract()
        book_price = response.css('div.price > div.price-new > span.value::text').extract() 
        
        with open('books_data.txt', 'a', encoding='utf-8') as file:
            for name, author, publisher, price in zip(book_names, book_authors, book_publishers, book_price):
                if "Platin Üyelik" in name:  
                    author = " "
                    name = " "
                    publisher = " "
                    
                data = f"Name: {name}\nAuthor: {author}\nPublisher: {publisher}\nPrice: {price}\n\n"
                file.write(data)
       
        next_page = response.css('a.next::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
