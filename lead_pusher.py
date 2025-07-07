from agents import acquisition

if __name__ == '__main__':
    leads = acquisition.scrape_leads('https://jsonplaceholder.typicode.com/users')
    if leads:
        acquisition.push_to_sheet(leads)
