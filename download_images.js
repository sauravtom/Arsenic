var Scraper = require('images-scraper')
  , bing = new Scraper.Bing();
 

var fs = require('fs'),
    request = require('request');

var search_term = process.argv[2];
var number_of_images = process.argv[3];

// process.argv.forEach(function (val, index, array) {
//   console.log(index + ': ' + val);
//   number_of_images = val;
// });

var download = function(uri, filename, callback){
  request.head(uri, function(err, res, body){
    //console.log('content-type:', res.headers['content-type']);
    //console.log('content-length:', res.headers['content-length']);

    request(uri).pipe(fs.createWriteStream(filename)).on('close', callback);
  });
};

bing.list({
    keyword: search_term,
    num: number_of_images,
    detail: true
})
.then(function (res) {
    console.log('first '+ number_of_images +' results from bing', res[0]['url']);
    console.log(res.length);
    for(i=0;i<res.length;i++){
    	var random_string = Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 5);
    	console.log(res[i]['url']);
    	download(res[i]['url'], 'oven/temp/slide_'+i+'.png', function(){
    	  console.log('downloaded' + res['url']);
    	});
    }
    
}).catch(function(err) {
    console.log('err',err);
})