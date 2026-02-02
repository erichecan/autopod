from server.services.image_gen import ImageGenService

service = ImageGenService()

def test_variety():
    print("Testing Keyword: Cottagecore (Expected: Botanical/Nature)")
    # Force keywords to match the service's logic
    urls_1 = service.generate_batch("Cottagecore Botanical Nature", count=3)
    print(urls_1)
    
    print("\nTesting Keyword: Cyberpunk (Expected: Neon/Tech)")
    urls_2 = service.generate_batch("Cyberpunk Neon Tech", count=3)
    print(urls_2)
    
    print("\nTesting Keyword: Minimalist (Expected: Clean)")
    urls_3 = service.generate_batch("Minimalist Typography", count=3)
    print(urls_3)

if __name__ == "__main__":
    test_variety()
