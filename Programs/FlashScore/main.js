const axios = require('axios')
const cheerio = require('cheerio')

axios.get('https://www.flashscore.ru/hockey/').then(html => {
    const $ = cheerio.load(html.data)
    var text1 = ''
    $('.event__participant--home').each((i, elem) => {
        text1 += `${$(elem).text()}\n`
    })
    var text2 = ''
    $('.event__participant--away').each((i, elem) => {
        text2 += `${$(elem).text()}\n`
    })
    console.log(`${text1} ${text2}`)
})