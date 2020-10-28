from bs4 import BeautifulSoup
import sys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class downloader(object):

    def __init__(self):
        self.server = 'https://www.mycareersfuture.gov.sg'
        self.target = 'https://www.mycareersfuture.gov.sg/search?search=Java&salary=6000&sortBy=new_posting_date&page='
        self.companynames = []
        self.urls = []
        self.nums = 0
        self.title = []
        self.location = []
        self.perm = []
        self.experience = []
        self.numApplication = []
        self.salary = []
        self.postdate = []

    def get_download_url(self):

        for x in range(0, 99):
            driver = webdriver.Chrome()
            url = self.target + str(x)
            driver.get(url)
            timeout = 40
            try:
                element_present = EC.presence_of_element_located((By.ID, 'job-card-0'))
                WebDriverWait(driver, timeout).until(element_present)
            except TimeoutException:
                print("Timed out waiting for page to load")
            content = BeautifulSoup(driver.page_source, "html.parser")
            driver.quit()

            a = content.find_all("div", "card relative")
            self.nums += len(a[:])
            for each in a[:]:
                link = self.server + each.a.get('href')
                self.urls.append(link)

            company = content.find_all("div", "pl3 JobCard__job-title-flex___2R-sW")
            for every in company[:]:
                companyName = every.p.string
                jobTitle = every.h1.string
                self.companynames.append(companyName)
                self.title.append(jobTitle)

            for job in content.find_all("div", "dn db-ns"):
                Area = job.p.string
                Type = job.p.next_sibling.string
                NumYear = job.find("p", "black-80 f6 fw4 mt0 mb1 dib pr3 icon-bw-period")
                if NumYear == None:
                    self.experience.append("null")
                else:
                    self.experience.append(NumYear.string)
                self.location.append(Area)
                self.perm.append(Type)

            for application in content.find_all("div", "w-40 ph3-ns ph0 order-3 dn db-l pt3"):
                self.numApplication.append(application.section.string)
                self.postdate.append(application.section.next_sibling.string)

            for salary in content.find_all("div", "lh-solid"):
                self.salary.append(salary.get_text())

            print("urls = " + str(len(self.urls)) + " years" + str(len(self.experience)))

    def writer(self, path, url, company, title, salary, experience, date, application, where, jobtype):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.writelines(company + ";" + title + ";" + salary + ";" + experience + ";" + date + ";" + application + ";" + where + ";" + jobtype + ";" + url)
            f.write('\n')

if __name__ == "__main__":
    dl = downloader()
    dl.get_download_url()
    for i in range(0,dl.nums-1):
        dl.writer('joblisting_6000.txt', dl.urls[i], dl.companynames[i], dl.title[i], dl.salary[i], dl.experience[i], dl.postdate[i], dl.numApplication[i], dl.location[i], dl.perm[i])
        sys.stdout.flush()

