//读取的文件名数组
const jsonFileNamesArr = ['assets/data/biology.json', 'assets/data/CS.json',
    'assets/data/economics.json', 'assets/data/math.json', 'assets/data/physics.json','assets/data/Geo_metadata.json'];
const subjectArr = ['生物学', '计算机科学', '经济学', '数学', '物理学','地理学'];
//学科与时间与论文数量关系的未处理数据
let subjectDataCountRow = [];
//学科与时间与论文数量关系处理后的数据
let subjectDataCount = [];
let subjectCounts = [];
// 存储读取到的JSON数据
let jsonDataArr = [];
let yearsArr = [];
let yearsCounts = [];

async function processJsonFiles() {
    for (const fileName of jsonFileNamesArr) {
        try {
            const response = await fetch(fileName);
            if (response.ok) {
                const data = await response.json();
                const subjectData = data.map(item => {
                    return item['Published: ']
                })
                jsonDataArr = [...jsonDataArr, ...data];
                subjectCounts.push(data.length);
                subjectDataCountRow.push(getDateData(subjectData))
                console.log(`已读取文件 ${fileName}`, subjectDataCountRow);
            } else {
                console.error(`读取文件 ${fileName} 时出错：${response.status}`);
            }
        } catch (error) {
            console.error(`读取文件 ${fileName} 时出错：${error.message}`);
        }
    }
}
const getDateData = (dateData) => {
// 创建一个对象来存储年份计数
    let yearCount = {};
    // 遍历日期字符串数组
    dateData.forEach((dateString) => {
        // 使用正则表达式提取年份部分
        let yearMatch = dateString.match(/\d{4}/);
        if (yearMatch && yearMatch.length > 0) {
            let year = yearMatch[0];
            // 如果年份已经存在，则增加计数，否则初始化为1
            if (yearCount[year]) {
                yearCount[year]++;
            } else {
                yearCount[year] = 1;
            }
        }
    });

// 提取年份和计数，存储在数组中
    yearsArr = Object.keys(yearCount); // 年份数组
    yearsCounts = Object.values(yearCount); // 年份次数数组
    // console.log("年份数组:", yearsArr);
    // console.log("年份次数数组:", yearsCounts);
    return yearCount
}
//绘制第一个图表
const printFirstChart = () => {
    const chartContainer = document.getElementById('firstChart');

// 初始化 ECharts 实例
    const myChart = echarts.init(chartContainer);

// 定义图表配置项和数据
    const option = {
        // 在这里配置图表的各种属性，如标题、X轴、Y轴、数据系列等
        title: {
            text: '不同年份的论文数量',
            left: 'center'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        xAxis: {
            data: yearsArr,
            axisTick: {
                alignWithLabel: true
            }
        },
        yAxis: {},
        series: [
            {
                name: '论文数量',
                type: 'bar',
                data: yearsCounts,
                itemStyle: {
                    color: '#007afd'
                },
                label: {
                    show: true, // 启用数据标签
                    position: 'top' // 设置数据标签的位置，可以根据需要调整
                },
            }
        ]
    };
    // 使用配置项设置图表
    myChart.setOption(option);
}

const printSecondChart = (names, counts) => {
    const chartContainer = document.getElementById('secondChart'); // 获取图表容器
    const myChart = echarts.init(chartContainer); // 初始化 ECharts 实例

    // 构建饼图的数据
    const pieData = names.map((name, index) => {
        return {
            name: name,
            value: counts[index]
        };
    });

    // 配置 ECharts 饼图的 option
    let option = {
        title: {
            text: '不同学科论文的数量占比',
            left: 'center'

        },
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b} : {c}' + '篇' + ' ({d}%)'
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            data: names
        },
        series: [
            {
                name: '学科占比',
                type: 'pie',
                radius: '55%',
                center: ['50%', '60%'],
                data: pieData,
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };

    // 使用配置项设置图表
    myChart.setOption(option);
}

const printThirdChart = (legend, xData, seriesData) => {
    const chartContainer = document.getElementById('thirdChart');
// 初始化 ECharts 实例
    const myChart = echarts.init(chartContainer);
    let option = {
        color: ['#80FFA5', '#00DDFF', '#37A2FF', '#FF0087', '#FFBF00','#845EC2'],
        title: {
            text: '各个学科文章数量随时间的变化关系'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                label: {
                    backgroundColor: '#6a7985'
                }
            }
        },
        legend: {
            data: legend,
            left: 520
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: [
            {
                type: 'category',
                boundaryGap: false,
                data: xData
            }
        ],
        yAxis: [
            {
                type: 'value'
            }
        ],
        series: [
            {
                name: '生物学',
                type: 'line',
                stack: 'Total',
                smooth: true,
                lineStyle: {
                    width: 0
                },
                showSymbol: false,
                areaStyle: {
                    opacity: 0.8,
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        {
                            offset: 0,
                            color: 'rgb(128, 255, 165)'
                        },
                        {
                            offset: 1,
                            color: 'rgb(1, 191, 236)'
                        }
                    ])
                },
                emphasis: {
                    focus: 'series'
                },
                data:seriesData[0]
            },
            {
                name: '计算机科学',
                type: 'line',
                stack: 'Total',
                smooth: true,
                lineStyle: {
                    width: 0
                },
                showSymbol: false,
                areaStyle: {
                    opacity: 0.8,
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        {
                            offset: 0,
                            color: 'rgb(0, 221, 255)'
                        },
                        {
                            offset: 1,
                            color: 'rgb(77, 119, 255)'
                        }
                    ])
                },
                emphasis: {
                    focus: 'series'
                },
                data: seriesData[1]
            },
            {
                name: '经济学',
                type: 'line',
                stack: 'Total',
                smooth: true,
                lineStyle: {
                    width: 0
                },
                showSymbol: false,
                areaStyle: {
                    opacity: 0.8,
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        {
                            offset: 0,
                            color: 'rgb(55, 162, 255)'
                        },
                        {
                            offset: 1,
                            color: 'rgb(116, 21, 219)'
                        }
                    ])
                },
                emphasis: {
                    focus: 'series'
                },
                data: seriesData[2]
            },
            {
                name: '数学',
                type: 'line',
                stack: 'Total',
                smooth: true,
                lineStyle: {
                    width: 0
                },
                showSymbol: false,
                areaStyle: {
                    opacity: 0.8,
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        {
                            offset: 0,
                            color: 'rgb(255, 0, 135)'
                        },
                        {
                            offset: 1,
                            color: 'rgb(135, 0, 157)'
                        }
                    ])
                },
                emphasis: {
                    focus: 'series'
                },
                data: seriesData[3]
            },
            {
                name: '物理学',
                type: 'line',
                stack: 'Total',
                smooth: true,
                lineStyle: {
                    width: 0
                },
                showSymbol: false,
                label: {
                    show: true,
                    position: 'top'
                },
                areaStyle: {
                    opacity: 0.8,
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        {
                            offset: 0,
                            color: 'rgb(255, 191, 0)'
                        },
                        {
                            offset: 1,
                            color: 'rgb(224, 62, 76)'
                        }
                    ])
                },
                emphasis: {
                    focus: 'series'
                },
                data: seriesData[4]
            },
            {
                name: '地理学',
                type: 'line',
                stack: 'Total',
                smooth: true,
                lineStyle: {
                    width: 0
                },
                showSymbol: false,
                label: {
                    show: true,
                    position: 'top'
                },
                areaStyle: {
                    opacity: 0.8,
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        {
                            offset: 0,
                            color: '#845EC2'
                        },
                        {
                            offset: 1,
                            color: '#D65DB1'
                        }
                    ])
                },
                emphasis: {
                    focus: 'series'
                },
                data: seriesData[4]
            }
        ]
    };
    myChart.setOption(option);
}

const sortData = (subjectObj) => {
    let arr = []
    yearsArr.forEach((item, index) => {
        if (subjectObj[item]) {
            arr.push(subjectObj[item])
        } else {
            arr.push(0)
        }
    })
    return arr
}

// 调用函数开始处理JSON文件
processJsonFiles().then(() => {
    let dateData = jsonDataArr.map(item => {
        return item['Published: ']
    })
    getDateData(dateData);
    printFirstChart();
    printSecondChart(subjectArr, subjectCounts);
    subjectDataCount = subjectDataCountRow.map(item => {
        return sortData(item)
    })
    // console.log(subjectDataCount)
    printThirdChart(subjectArr,yearsArr,subjectDataCount);
    console.log(yearsArr,subjectArr,subjectDataCount)
});

