
function onSuccess(jsonData){
    console.log(jsonData)

    var yourVlSpec = {
        $schema: 'https://vega.github.io/schema/vega-lite/v5.json',
        description: 'A simple bar chart with embedded data.',
        data: {
          values: jsonData
        },
        mark: 'bar',
        encoding: {
          x: {field: 'audio', type: 'quantitative'},
          y: {field: 'motion', type: 'quantitative'}
        }
      };
      vegaEmbed('#vis', yourVlSpec);
}

let url = window.location.href
let index = url.indexOf("?")
let parameters = ""

if (index!=-1){
    parameters = url.slice(index)
}
console.log("bruh")
jQuery.ajax({
    dataType: "json",
    method: "GET",
    url: "get" + parameters,
    success:(resultData) => onSuccess(resultData)
})