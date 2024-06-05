
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
        width: 700,
        title: 'hi',
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
                timeUnit: {unit:"hoursminutes",step:30},
                type: 'temporal',
                axis: {tickCount:48},
                scale: {
                    domain: [{hours: 0, minutes:0}, {hours: 23, minutes:59}]
                }
            },
            y: {aggregate: "sum", 
                type: 'quantitative',
                field: 'value',
                title: 'Motion/Audio Levels',
            }, 
            color: {
                field: "key",
                type: "nominal",
                scale: {
                    domain: ["motion", "audio"]
                },
                
            title: "Input Type"
            }
        },
        
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