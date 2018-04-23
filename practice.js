let cheerio = require('cheerio')
let axios = require('axios');
let jsonframe = require('jsonframe-cheerio');
let fs = require('fs');
axios.get('https://www.producthunt.com');.then((response)=>{
      if(response.status === 200){
        var html = response.data;
        let $ = cheerio.load(html);
        jsonframe($);
        fs.writeFileSync('ph.html', html);

        var productsFrame = {
          "products":{
            "selector":"ul.postsList_3n2Ck li",
            "data":[{
              "name": ".content_3Qj0y .title_24w6f",
              "description": ".content_3Qj0y .subtle_fyrho",
              "image":{
                "selector":"img",
                "attr":"src"
              },
              "upvotes":"[data-test=vote-button] .buttonContainer_1ROJn",
              "comments":"[data-test=vote-button] + a .buttonContainer_1ROJn"
            }]
          }
        };
        var products = $('body').scrape(productsFrame);
        fs.writeFileSync("products.json",JSON.stringify(products,null,2));
          }
        },(error)=> {
          console.log("Humm: ", error);
        });
