// **********************DATABASE**********************

const { MongoClient } = require('mongodb');
// or as an es module:
// import { MongoClient } from 'mongodb'

// Connection URL
const url = 'mongodb+srv://admin:4OHdmJqc0fWC7gTF@cluster0.egwho.mongodb.net/myFirstDatabase?retryWrites=true&w=majority';
const client = new MongoClient(url);

// **********************CONST**********************
const moment = require('moment')
moment.locale('en');

const axios = require('axios')
const cheerio = require('cheerio')

const VkBot = require('node-vk-bot-api');

const bot = new VkBot({
    token: '21e584050aa91b1088821b155ec5ad48019add851b84faa19a6b7f93c4f8ed6689bec1a51943537f7f93b'
});

const Markup = require('node-vk-bot-api/lib/markup');

const Session = require('node-vk-bot-api/lib/session');

const Scene = require('node-vk-bot-api/lib/scene');

const Stage = require('node-vk-bot-api/lib/stage');

bot.startPolling();
console.log('\nThe bot has been successfully launched and ready to work.')

const nodebot = 'ZernoBot'

client.connect();

console.log('Connected successfully to server');

const db = client.db(nodebot);

const collUsers = db.collection('users');

const collDate = db.collection('date');

const collDateSum = db.collection('datesum');
// **********************SCENE**********************

const calc = new Scene('calc',
  (ctx) => {
    ctx.scene.next();
    ctx.reply('Сколько тонн вы занесли?🌾');
  },
  (ctx) => {
      ton = ctx.message.text

    ctx.scene.next();
    ctx.reply(`Сколько стоит тонна?💵`);
  },
  (ctx) => {
      course = ctx.message.text
      finRUB = ton * course

    ctx.scene.next();
    ctx.reply(`Сколько человек работало?👥`);
  },
  (ctx) => {
      people = ctx.message.text
      finalRUB = finRUB / people

    // courseUSD = text
    // finUSD = 
    // finalUSD = 

    ctx.scene.leave();

    axios.get('https://www.banki.ru/products/currency/usd/').then(html => {
        const $ = cheerio.load(html.data)
        var courseUSD = ''
        $('body > div.layout-wrapper.padding-top-default.bg-white.position-relative > div.layout-columns-wrapper > main > section:nth-child(4) > div.currency-table > table > tbody > tr > td.currency-table__rate.currency-table__darken-bg > div.currency-table__large-text').each((i, elem) => {
            courseUSD += `${$(elem).text()}\n`
        })
        courseUSDfin = courseUSD.split(',').join('.')
        finUSD = (finRUB / courseUSDfin).toFixed(1);
        finalUSD = (finalRUB / courseUSDfin).toFixed(1);
        ctx.reply(`Каждый заработал по ${finalRUB}₽(${finalUSD}$)💸\nВсего вы заработали ${finRUB}₽(${finUSD}$)💸`);
    })

    // ctx.reply(`${text} Каждый заработал по ${finalRUB}₽💸\nВсего вы заработали ${finRUB}₽💸`);
  }
);

const memoryplus = new Scene('memoryplus',
  (ctx) => {
    ctx.scene.next();
    ctx.reply(`На сколько тонн?🌾`);
  },
  async (ctx) => {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();
    today = dd + '/' + mm + '/' + yyyy;

    const memoryDay = await collDate.findOne({ id: ctx.message.peer_id })
    await collDate.updateOne({ date: today }, { $inc: {number: Number(ctx.message.text)} })
    const memoryDaySum = await collDateSum.findOne({ id: ctx.message.peer_id })
    await collDateSum.updateOne({ id: ctx.message.peer_id }, { $inc: {number: Number(ctx.message.text)} })

    ctx.scene.leave();
    ctx.reply(`Хорошо, я запомнил💡\nЧтобы узнать сколько вы уже занесли Нажмите кнопку "Всего"📑`);
  }
);

const session = new Session();
const stage = new Stage(calc, memoryplus);

bot.use(session.middleware());
bot.use(stage.middleware());

// ''

bot.command(/начать/i, (ctx) => {    
    collUsers.insertOne({
        id: ctx.message.peer_id,
        data: 'https://vk.com/foaf.php?id=' + ctx.message.peer_id
    })
    ctx.reply('Есть десептиконы...есть автоботы...а есть зерноботы😹\n\n⚠📜Как пользоваться ботом:\n\n♻Перед началом работы нажмите кнопку "Сброс". Эту кнопку нужно нажимать каждый день, когда будут заказы, перед началом работы. После этого можете воспользоваться всеми остальными функциями.\n📞С помощью кнопки "Заказ" бот будет запоминать сколько тонн вы занесли.\n📑Кнопка "Всего" будет выводить сколько тонн вы уже занесли.\n💸Кнопка "Прибыль" запускает калькулятор прибыли.\n\n🖊✉Если есть вопросы, писать сюда:\nhttps://vk.com/r_alexandrovich\n\nНажмите, чтобы начать работу с ботом:', null, Markup.keyboard(
      ['Сброс♻']
      )
    .inline())
});

bot.command(/всего/i, async (ctx) => {    
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();
    today = dd + '/' + mm + '/' + yyyy;

    const memoryDay = await collDate.findOne({ date: today })
    const memoryDaySum = await collDateSum.findOne({ id: ctx.message.peer_id })
    ctx.reply(`Cегодня вы занесли: ${memoryDay.number}🌾\nЗа всё время вы занесли: ${memoryDaySum.number}🌾`, null, Markup.keyboard(
      ['Прибыль💸']
      )
    .inline());
});

bot.command(/сброс/i, async ctx => {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();
    today = dd + '/' + mm + '/' + yyyy;
    
    await collDate.insertOne({
        id: ctx.message.peer_id,
        number: 0,
        date: today
    })
    await collDateSum.insertOne({
        id: ctx.message.peer_id,
        number: 0
    })
    ctx.reply('Данные сохранены✔', null, Markup.keyboard(
      ['Заказ📞']
      )
    .inline())
});

bot.command(/заказ/i, async (ctx) => {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();
    today = dd + '/' + mm + '/' + yyyy;

    const memoryDay = await collDate.findOne({ date: today })
    ctx.scene.enter('memoryplus');
});

bot.command(/прибыль/i, (ctx) => {
    ctx.scene.enter('calc');
})

bot.command(/погода/i, (ctx) => {
  var day = moment().format('DD');
    var monthToParser = moment().format('MMMM');
    var monthToMessage = moment().format('MMM');
    var monthToParserLowerCase = monthToParser.toLowerCase()
    var monday = moment().startOf("isoWeek").format('DD');
    var tuesday = moment().startOf("isoWeek").add(1, "days").format('DD');
    var wednesday = moment().startOf("isoWeek").add(2, "days").format('DD');
    var thursday = moment().startOf("isoWeek").add(3, "days").format('DD');
    var friday = moment().startOf("isoWeek").add(4, "days").format('DD');
    var saturday = moment().startOf("isoWeek").add(5, "days").format('DD');
    var sunday = moment().startOf("isoWeek").add(6, "days").format('DD');
    function Monday(){
        axios.get(`https://pogoda.mail.ru/prognoz/rostov-na-donu/${monday}-${monthToParserLowerCase}/`).then(html => {
        const $ = cheerio.load(html.data)

        var OneGrad = ''
        $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__temperature').each((i, elem) => {
            OneGrad += `${$(elem).text()}`
        })
        var OneKak = ''
        $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
            OneKak += `${$(elem).text()}`
        })

        var TwoGrad = ''
        $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(2) > div.day__temperature').each((i, elem) => {
            TwoGrad += `${$(elem).text()}`
        })
        var TwoKak = ''
        $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
            TwoKak += `${$(elem).text()}`
        })

        var ThreeGrad = ''
        $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(3) > div.day__temperature').each((i, elem) => {
            ThreeGrad += `${$(elem).text()}`
        })
        var ThreeKak = ''
        $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
            ThreeKak += `${$(elem).text()}`
        })

        var FourGrad = ''
        $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(4) > div.day__temperature').each((i, elem) => {
            FourGrad += `${$(elem).text()}`
        })
        var FourKak = ''
        $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
            FourKak += `${$(elem).text()}`
        })
        
        var osadki = ''
        $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div:nth-child(9) > span').each((i, elem) => {
            osadki += `${$(elem).text()}`
        })

        ctx.reply(`------------------------------------------\nПонедельник(${monday} ${monthToMessage})\n\nНочью: ${OneGrad}(${OneKak})\nУтром: ${TwoGrad}(${TwoKak})\nДнём: ${ThreeGrad}(${ThreeKak})\nВечером: ${FourGrad}(${FourKak})\nВероятность осадков: ${osadki}\n------------------------------------------`)
    })
}
setTimeout(Monday, 0)

    function Tuesday(){
        axios.get(`https://pogoda.mail.ru/prognoz/rostov-na-donu/${tuesday}-${monthToParserLowerCase}/`).then(html => {
        const $ = cheerio.load(html.data)

        var OneGrad = ''
        $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__temperature').each((i, elem) => {
            OneGrad += `${$(elem).text()}`
        })
        var OneKak = ''
        $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
            OneKak += `${$(elem).text()}`
        })

        var TwoGrad = ''
        $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(2) > div.day__temperature').each((i, elem) => {
            TwoGrad += `${$(elem).text()}`
        })
        var TwoKak = ''
        $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
            TwoKak += `${$(elem).text()}`
        })

        var ThreeGrad = ''
        $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(3) > div.day__temperature').each((i, elem) => {
            ThreeGrad += `${$(elem).text()}`
        })
        var ThreeKak = ''
        $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
            ThreeKak += `${$(elem).text()}`
        })

        var FourGrad = ''
        $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(4) > div.day__temperature').each((i, elem) => {
            FourGrad += `${$(elem).text()}`
        })
        var FourKak = ''
        $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
            FourKak += `${$(elem).text()}`
        })
        
        var osadki = ''
        $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div:nth-child(9) > span').each((i, elem) => {
            osadki += `${$(elem).text()}`
        })

        ctx.reply(`------------------------------------------\nВторник(${tuesday} ${monthToMessage})\n\nНочью: ${OneGrad}(${OneKak})\nУтром: ${TwoGrad}(${TwoKak})\nДнём: ${ThreeGrad}(${ThreeKak})\nВечером: ${FourGrad}(${FourKak})\nВероятность осадков: ${osadki}\n------------------------------------------`)
    })
}
setTimeout(Tuesday, 1500)

function Wednesday(){
    axios.get(`https://pogoda.mail.ru/prognoz/rostov-na-donu/${wednesday}-${monthToParserLowerCase}/`).then(html => {
    const $ = cheerio.load(html.data)

    var OneGrad = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__temperature').each((i, elem) => {
        OneGrad += `${$(elem).text()}`
    })
    var OneKak = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
        OneKak += `${$(elem).text()}`
    })

    var TwoGrad = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(2) > div.day__temperature').each((i, elem) => {
        TwoGrad += `${$(elem).text()}`
    })
    var TwoKak = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
        TwoKak += `${$(elem).text()}`
    })

    var ThreeGrad = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(3) > div.day__temperature').each((i, elem) => {
        ThreeGrad += `${$(elem).text()}`
    })
    var ThreeKak = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
        ThreeKak += `${$(elem).text()}`
    })

    var FourGrad = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(4) > div.day__temperature').each((i, elem) => {
        FourGrad += `${$(elem).text()}`
    })
    var FourKak = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
        FourKak += `${$(elem).text()}`
    })
    
    var osadki = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div:nth-child(9) > span').each((i, elem) => {
        osadki += `${$(elem).text()}`
    })

    ctx.reply(`------------------------------------------\nСреда(${wednesday} ${monthToMessage})\n\nНочью: ${OneGrad}(${OneKak})\nУтром: ${TwoGrad}(${TwoKak})\nДнём: ${ThreeGrad}(${ThreeKak})\nВечером: ${FourGrad}(${FourKak})\nВероятность осадков: ${osadki}\n------------------------------------------`)
})
}
setTimeout(Wednesday, 3000)

function Thursday(){
    axios.get(`https://pogoda.mail.ru/prognoz/rostov-na-donu/${thursday}-${monthToParserLowerCase}/`).then(html => {
    const $ = cheerio.load(html.data)

    var OneGrad = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__temperature').each((i, elem) => {
        OneGrad += `${$(elem).text()}`
    })
    var OneKak = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
        OneKak += `${$(elem).text()}`
    })

    var TwoGrad = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(2) > div.day__temperature').each((i, elem) => {
        TwoGrad += `${$(elem).text()}`
    })
    var TwoKak = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
        TwoKak += `${$(elem).text()}`
    })

    var ThreeGrad = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(3) > div.day__temperature').each((i, elem) => {
        ThreeGrad += `${$(elem).text()}`
    })
    var ThreeKak = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
        ThreeKak += `${$(elem).text()}`
    })

    var FourGrad = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(4) > div.day__temperature').each((i, elem) => {
        FourGrad += `${$(elem).text()}`
    })
    var FourKak = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
        FourKak += `${$(elem).text()}`
    })
    
    var osadki = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div:nth-child(9) > span').each((i, elem) => {
        osadki += `${$(elem).text()}`
    })

    ctx.reply(`------------------------------------------\nЧетверг(${thursday} ${monthToMessage})\n\nНочью: ${OneGrad}(${OneKak})\nУтром: ${TwoGrad}(${TwoKak})\nДнём: ${ThreeGrad}(${ThreeKak})\nВечером: ${FourGrad}(${FourKak})\nВероятность осадков: ${osadki}\n------------------------------------------`)
})
}
setTimeout(Thursday, 4500)

function Friday(){
    axios.get(`https://pogoda.mail.ru/prognoz/rostov-na-donu/${friday}-${monthToParserLowerCase}/`).then(html => {
    const $ = cheerio.load(html.data)

    var OneGrad = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__temperature').each((i, elem) => {
        OneGrad += `${$(elem).text()}`
    })
    var OneKak = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
        OneKak += `${$(elem).text()}`
    })

    var TwoGrad = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(2) > div.day__temperature').each((i, elem) => {
        TwoGrad += `${$(elem).text()}`
    })
    var TwoKak = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
        TwoKak += `${$(elem).text()}`
    })

    var ThreeGrad = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(3) > div.day__temperature').each((i, elem) => {
        ThreeGrad += `${$(elem).text()}`
    })
    var ThreeKak = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
        ThreeKak += `${$(elem).text()}`
    })

    var FourGrad = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(4) > div.day__temperature').each((i, elem) => {
        FourGrad += `${$(elem).text()}`
    })
    var FourKak = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
        FourKak += `${$(elem).text()}`
    })
    
    var osadki = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div:nth-child(9) > span').each((i, elem) => {
        osadki += `${$(elem).text()}`
    })

    ctx.reply(`------------------------------------------\nПятница(${friday} ${monthToMessage})\n\nНочью: ${OneGrad}(${OneKak})\nУтром: ${TwoGrad}(${TwoKak})\nДнём: ${ThreeGrad}(${ThreeKak})\nВечером: ${FourGrad}(${FourKak})\nВероятность осадков: ${osadki}\n------------------------------------------`)
})
}
setTimeout(Friday, 6000)

function Saturday(){
    axios.get(`https://pogoda.mail.ru/prognoz/rostov-na-donu/${saturday}-${monthToParserLowerCase}/`).then(html => {
    const $ = cheerio.load(html.data)

    var OneGrad = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__temperature').each((i, elem) => {
        OneGrad += `${$(elem).text()}`
    })
    var OneKak = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
        OneKak += `${$(elem).text()}`
    })

    var TwoGrad = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(2) > div.day__temperature').each((i, elem) => {
        TwoGrad += `${$(elem).text()}`
    })
    var TwoKak = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
        TwoKak += `${$(elem).text()}`
    })

    var ThreeGrad = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(3) > div.day__temperature').each((i, elem) => {
        ThreeGrad += `${$(elem).text()}`
    })
    var ThreeKak = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
        ThreeKak += `${$(elem).text()}`
    })

    var FourGrad = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(4) > div.day__temperature').each((i, elem) => {
        FourGrad += `${$(elem).text()}`
    })
    var FourKak = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
        FourKak += `${$(elem).text()}`
    })
    
    var osadki = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div:nth-child(9) > span').each((i, elem) => {
        osadki += `${$(elem).text()}`
    })

    ctx.reply(`------------------------------------------\nСуббота(${saturday} ${monthToMessage})\n\nНочью: ${OneGrad}(${OneKak})\nУтром: ${TwoGrad}(${TwoKak})\nДнём: ${ThreeGrad}(${ThreeKak})\nВечером: ${FourGrad}(${FourKak})\nВероятность осадков: ${osadki}\n------------------------------------------`)
})
}
setTimeout(Saturday, 7500)

function Sunday(){
    axios.get(`https://pogoda.mail.ru/prognoz/rostov-na-donu/${sunday}-${monthToParserLowerCase}/`).then(html => {
    const $ = cheerio.load(html.data)

    var OneGrad = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__temperature').each((i, elem) => {
        OneGrad += `${$(elem).text()}`
    })
    var OneKak = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
        OneKak += `${$(elem).text()}`
    })

    var TwoGrad = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(2) > div.day__temperature').each((i, elem) => {
        TwoGrad += `${$(elem).text()}`
    })
    var TwoKak = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
        TwoKak += `${$(elem).text()}`
    })

    var ThreeGrad = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(3) > div.day__temperature').each((i, elem) => {
        ThreeGrad += `${$(elem).text()}`
    })
    var ThreeKak = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
        ThreeKak += `${$(elem).text()}`
    })

    var FourGrad = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(4) > div.day__temperature').each((i, elem) => {
        FourGrad += `${$(elem).text()}`
    })
    var FourKak = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div:nth-child(3) > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div.day__description > span:nth-child(1)').each((i, elem) => {
        FourKak += `${$(elem).text()}`
    })
    
    var osadki = ''
    $('body > div.g-layout.layout.js-module > div.sticky-springs.js-springs__group.js-module > div.block.block_selected > div > div > div > div > div.cols__column__item.cols__column__item_2-1.cols__column__item_2-1_ie8 > div:nth-child(1) > div:nth-child(9) > span').each((i, elem) => {
        osadki += `${$(elem).text()}`
    })

    ctx.reply(`------------------------------------------\nВоскресение(${sunday} ${monthToMessage})\n\nНочью: ${OneGrad}(${OneKak})\nУтром: ${TwoGrad}(${TwoKak})\nДнём: ${ThreeGrad}(${ThreeKak})\nВечером: ${FourGrad}(${FourKak})\nВероятность осадков: ${osadki}\n------------------------------------------`)
})
}
setTimeout(Sunday, 9000)
})