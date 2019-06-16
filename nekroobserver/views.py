## VIEWS FOR PROJECT NEKROBSERVER
#############################################################

from django.shortcuts import render

# Create your views here.

#main page / HOME
def index (request):
    page = {'header':'In vita mors certa est',
            }
    return render(request, 'home.html',context={'page':page})


# about
def about (request):
    page = {'header':'Kim jesteśmy?',
            'title':'O nas'
            }
    return render(request, 'about.html', context={'page':page})

# source
def source (request):
    page = {}
    return render(request, 'source.html', context={'page':page})

#querry
def home_search (request, name):


    from requests_html import HTML, HTMLSession
    from datetime import date

    def crawler(input):
        day = date.today().day
        month = date.today().month
        source = ['ppma_dzpo', 'ppma_krak']

        # nekrologi.net
        # dz pol
        url1 = 'https://www.nekrologi.net/szukaj?publication={source}&keywords=&date_limit=7&date=&type=all_memorial&_fstatus=search&order_by='.format(
            source=source[0])
        # krakowska
        url2 = 'https://www.nekrologi.net/szukaj?publication={source}&keywords=&date_limit=7&date=&type=all_memorial&_fstatus=search&order_by='.format(
            source=source[1])

        # gazeta wyborcza
        url3 = 'http://nekrologi.wyborcza.pl/0,10,,1,0,100,,,,KR,,{day},{month},2019.html'.format(day=day,
                                                                                                  month=month - 1)
        output = []
        # obiekt parser
        session = HTMLSession()

        # pobieranie strony
        page1 = session.get(url1)
        html = HTML(html=page1.text)

        noticeContent = html.find('div.notice')
        for keyword in input:
            for el in noticeContent:
                if keyword in el.find('h2.noticeName')[0].text or keyword in el.find('p.shortText')[0].text:
                    output.append('{url1}'.format(url1=url1))
        page2 = session.get(url2)
        htm2 = HTML(html=page2.text)

        noticeContent = htm2.find('div.notice')
        for el in noticeContent:
            for keyword in input:
                if keyword in el.find('h2.noticeName')[0].text or keyword in el.find('p.shortText')[0].text:
                    output.append('{url1}'.format(url1=url2))

        page3 = session.get(url3)
        html3 = HTML(html=page3.text)
        res = html3.find('li.premium')[0]
        for keyword in input:
            if keyword in res.text:
                output.append('{url1}'.format(url1=url3))

        return output


    output = crawler([name])
    lenght = len(output)

    page = {'header': 'In vita mors certa est',
            'keyword': name, 'output':output, 'lenght':lenght}

    return render(request, 'home_search.html', context={'page':page,})