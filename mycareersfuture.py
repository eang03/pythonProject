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

        for x in range(0, 100):
            driver = webdriver.Chrome()
            url = self.target + str(x)
            driver.get(url)
            timeout = 50
            try:
                element_present = EC.presence_of_element_located((By.ID, 'job-card-0'))
                WebDriverWait(driver, timeout).until(element_present)
            except TimeoutException:
                print("Timed out waiting for page to load")
            content = BeautifulSoup(driver.page_source, "html.parser")
            driver.quit()

            a = content.find_all("div", "card relative")

            for each in a[:]:
                link = self.server + each.a.get('href')
                companyName = each.a.p.string
                jobTitle = each.a.h1.string

                self.urls.append(link)
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
                Applicant = application.section
                if Applicant.string == None:
                    self.numApplication.append("null")

                else:
                    self.numApplication.append(Applicant.string)

                Post = application.section.next_sibling
                if Post == None:
                    self.postdate.append("null")
                else:
                    self.postdate.append(Post.string)

            for salary in content.find_all("div", "lh-solid"):
                if salary.get_text() == None:
                    self.salary.append("null")
                else:
                    self.salary.append(salary.get_text())

            print("urls = " + str(len(self.urls)) + " years" + str(len(self.experience)))
            for i in range(self.nums, len(dl.urls[:])):
                dl.writer('joblisting_6000.txt', dl.urls[i], dl.companynames[i], dl.title[i], dl.salary[i],
                          dl.experience[i], dl.postdate[i], dl.numApplication[i])
                sys.stdout.flush()

            print("Done written index " + str(self.nums) + " to " + str(len(dl.urls[:])-1))
            self.nums = len(dl.urls[:])

    def writer(self, path, url, company, title, salary, experience, date, application):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.writelines(company + ";" + title + ";" + salary + ";" + experience + ";" + date + ";" + application + ";" + url)
            f.write('\n')

if __name__ == "__main__":
    dl = downloader()
    dl.get_download_url()


