from bs4 import BeautifulSoup
import urllib2

petition72_content = (
    urllib2
        .urlopen("http://boxitvn.blogspot.com/2013/01/kien-nghi-ve-sua-oi-hien-phap-1992.html")
        .read()
  )

petition72_soup = BeautifulSoup(petition72_content)

petition72_post = petition72_soup.find_all("div", class_="post-body entry-content")[0]
petition72_dict = dict([ [el.strip() for el in ''.join([e.replace('\n', ' ').replace('\r', '') for e in li.find_all(text=True)]).split(",", 1)]
                    for li in petition72_post.ol.find_all('li')])

newpetition_content = (
    urllib2
        .urlopen("http://www.diendan.org/viet-nam/thu-gui-bchtu-va-dang-vien-dcsvn")
        .read()

    )
newpetition_soup = BeautifulSoup(newpetition_content)

newpetition_post = newpetition_soup.find_all("div", id="parent-fieldname-text-d823166504da4795a295fdf072f06142")[0]
newpetition_dict = dict([ [el.strip() for el in ''.join([e.replace('\n', ' ').replace('\r', '') for e in li.find_all(text=True)]).split(",", 1)]
                    for li in newpetition_post.ol.find_all('li')])

common = {k: v for k, v in petition72_dict.items() if k in newpetition_dict}
petition72_only = {k: v for k, v in petition72_dict.items() if k not in newpetition_dict}
newpetition_only = {k: v for k, v in newpetition_dict.items() if k not in petition72_dict}

file = open("petitioner_names.txt", "wb")
file.write("Names that appear in both\n")
for k, v in common.items():
    file.write(k.encode('utf8') + ", " + v.encode('utf8') + "\n")
file.write("\nNames that appear in petition 72 only\n")
for k, v in petition72_only.items():
    file.write(k.encode('utf8') + ", " + v.encode('utf8') + "\n")
file.write("\nNames that appear in new petition only\n")
for k, v in newpetition_only.items():
    file.write(k.encode('utf8') + ", " + v.encode('utf8') + "\n")
file.close()