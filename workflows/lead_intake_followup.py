from agents import acquisition, retention


def run_workflow():
    leads = acquisition.scrape_leads('https://jsonplaceholder.typicode.com/users')
    if leads:
        acquisition.push_to_sheet(leads)
        retention.send_followup('Follow up with new leads.')


if __name__ == '__main__':
    run_workflow()
