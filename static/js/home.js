
function onSuccess(jsonData){
    console.log(jsonData)

    // var yourVlSpec = {
    //     $schema: 'https://vega.github.io/schema/vega-lite/v5.json',
    //     description: 'A simple bar chart with embedded data.',
    //     data: {
    //       values: jsonData
    //     },
    //     mark: 'bar',
    //     encoding: {
    //       x: {field: 'audio', type: 'quantitative'},
    //       y: {field: 'motion', type: 'quantitative'}
    //     }
    //   };
    //TODO Should format jsonData to include the date separately so we don't have to extract it from the list of data
    var yourVlSpec = {
        $schema: 'https://vega.github.io/schema/vega-lite/v5.json',
        description: 'ROOM NAME (DATE)',
        mark: 'bar',
        data: {
            values: jsonData, 
            "format": {
            "parse": {"date": "utc:'%d %b %Y %H:%M:%S'"}
            }
        },

        transform: [
            {fold: ["motion", "audio"]}
        ],
        encoding: {
          x: {field: 'datetime', 
              timeUnit: "hoursminutes",
              type: 'ordinal'},
          y: {aggregate: "sum", 
              type: 'quantitative',
              field: 'value',
              title: 'bruh'
          }
        },
        color: {
          field: "key",
          type: "nominal",
          scale: {
            domain: ["motion", "audio"],
            range: ["#e7ba52", "#c7c7c7"]
          },
          title: "Weather type"
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