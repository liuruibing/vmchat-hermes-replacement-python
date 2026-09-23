/*#********************* 数据处理***************************************************#
#*********check_data(a)             --数据检查 ***********************************#
#*********trim_space(a)             --去除空格 ***********************************#
#*********dataHandle(a)             --空值处理成“--” *****************************#
#*********dataHandle0(a)            --空值处理成“0” ******************************#
#*********processing_Decimal(a,b)   --数据处理函数，保留小数点 **********************#
#*********toThousands(a,b)          --数据千分位处理 ******************************#
#*********to_thousands(a,b,c)          --数据千分位处理
*                                    (自定义无数据/空值返回数据) ********************#
#*********toPercent(a)              --数据百分化(默认保留两位,不可传参) **************#
#*********toPercentCustom(a,b)      --数据百分化(必须传入保留位数) ******************#
#*********to_percent(a,b,c)           --数据百分化
*                                   (必须传入保留位数，自定义无数据/空值返回数据) *****#
#*********getMin_Max(a[][])             --获取数据最大值和最小值 ***********************#
#*********splitString(a,size)       --截取字符串重组 *****************************#
#*********numberSum(a,b)            --数值字符串求和 *****************************#
#*********optionXAndX2(max)         --根据数值来来设置图表 X轴的距离
#*********abs(a)         --绝对值函数 避免导出pdf 时 wkhtmltopdf 不支持Match 函数的方法#
#*********sqrt(a)         --开平方根函数 避免导出pdf 时 wkhtmltopdf 不支持Match 函数的方法#
*#
#*******************************************************************************#
*/


//  去除字符串中的所有空格，包括圆角空格
//    @a  原数据
export function trim_space (a) {
    return String(a).toString().replace(String.fromCharCode(12288), '').replace(/\s*/g, '');
};

//    数据检查
//    @param  原数据
export function check_data (b) {
    b = trim_space(String(b) || "");
    if (b == undefined || b == "" || b == null || b == "undefined" || b == 'null') {
        return true;
    } else {
        return false;
    }
};


//    空值处理成“--”
//    @param  原数据
export function dataHandle (c) {
    if (check_data(c)) {
        c = '-';
    }
    return trim_space(c);
};

//    空值处理成“0”
//    @param  原数据
export function dataHandle0 (d) {
    if (check_data(d)) {
        d = 0;
    }
    return d;
};

//    数据处理函数，保留小数点
//    @param  原数据
//    @num  保留的精度
export function processing_Decimal (e, num1) {
    if (check_data(e)) {
        e = dataHandle0(e);
        return e;
    }
    if (isNaN(e)) {
        e = dataHandle0(e);
        console.info('MSG：数据源不是数值类型');
        return e;
    }
    if (isNaN(num1)) {
        e = dataHandle0(e);
        console.info('MSG：精度设置有误，精度num=' + num1);
        return e;
    } else {
        e = Number(e).toFixed(num1);
        return e;
    }
    //return param;

};

//    数据千分位处理
//    @param 原数据
export function toThousands (f, num2) {
    var result = '';
    if (check_data(f) || isNaN(f)) {
        console.info('MSG：数据源不是数值类型，数据：' + f)
        result = f;
    } else {
        if (isNaN(num2)) {
            console.info('MSG：精度设置有误，精度num=' + num2);
            result = f;
        } else {
            //使用正则表达式处理数据，每三位添加一个','
            result = Number(f).toFixed(num2).replace(/(\d)(?=(\d{3})+\.)/g, '$1,');
        }
    }
    return result;
};

/**
 * 处理数据千分位
 * @param f 原始数据
 * @param num2 精确位数
 * @param fmt 替代符
 * @returns {*|string}
 */
export function to_thousands (f, num2, fmt) {
    var result = '';
    if (check_data(f) || isNaN(f)) {
        console.info('MSG：数据源不是数值类型，数据：' + f)
        result = fmt;
    } else {
        if (isNaN(num2)) {
            console.info('MSG：精度设置有误，精度num=' + num2);
            result = f;
        } else {
            //使用正则表达式处理数据，每三位添加一个','
            result = Number(f).toFixed(num2).replace(/(\d)(?=(\d{3})+\.)/g, '$1,');
        }
    }
    return result;
};

//    数据百分化(默认展示两位)
//    @param 原数据
export function toPercent (g) {
    var result1;
    if (check_data(g) || isNaN(g)) {
        if (isNaN(g)) {
            console.info('MSG：原数据错误！\nCase：原数据不是数值！');
        }
        return result1 = '--';
    } else {
        result1 = Number(g * 100).toFixed(2);
        result1 += '%';
        return result1;
    }
};
export function toPercentCustom (newg, position) {
    var result1;
    if (check_data(newg) || isNaN(newg)) {
        if (isNaN(newg)) {
            console.info('MSG：原数据错误！\nCase：原数据不是数值！');
        }
        return result1 = '--';
    } else {
        if (isNaN(position)) {
            console.info('MSG:保留的位数错误! Case:位数[' + position + ']不是数值,请检查');
        }
        result1 = Number(newg * 100).toFixed(position);
        result1 += '%';
        return result1;
    }
};

/**
 * 数据百分化
 * @param newg 原始数据
 * @param position 保留小数位数
 * @param str 替代符
 * @returns {*}
 */
export function to_percent (newg, position, str) {
    var result1;
    if (check_data(newg) || isNaN(newg)) {
        if (isNaN(newg)) {
            console.info('MSG：原数据错误！\nCase：原数据[' + newg + ']不是数值！');
            result1 = str;
        }
    } else {
        if (isNaN(position)) {
            console.info('MSG:保留的位数错误! Case:位数[' + position + ']不是数值,请检查');
        }
        result1 = Number(newg * 100).toFixed(position);
        result1 += '%';
    }
    return result1;
};

//  获取数据最大值和最小值
//  最小值为原数据的最小值*0.9
//  最大值为原数据的最大值*1.1
//  参数 String[][]
export function getMin_Max (resultArray) {
    var value=[];
    if(resultArray == null || resultArray.length < 1){
        value = ["0","0"];
        return value;
    }
    var max = 0;
    var min = 0;
    var arrtp =[] ;
    for(var  i=0; i<resultArray.length; i++){
        arrtp = getMaxAndMin(resultArray[i]);
        if(i == 0){
            max = arrtp[0];
            min = arrtp[1];
        } else {
            if(arrtp[0] > max)
                max = arrtp[0];
            if(arrtp[1] < min)
                min = arrtp[1];
        }
    }
    if(max < 0) {
        max = max * 0.95;
    } else {
        max = max * 1.05;
    }
    if(min > 0) {
        min = min * 0.95;
    } else {
        min = min * 1.05;
    }

    return new Array(min, max);
};

//  参数 String[]
var getMaxAndMin=function (array) {
    var value=[];
    if(array == null || array.length < 1){
        value = [0 , 0];
        return value;
    }
    var max;
    var	min;
    max = min = Number(isEmpty(array[0])) ? "0" : Number(array[0]);
    for(var i=1; i<array.length; i++){
        var tp = Number(isEmpty(array[i])) ? "0" : Number(array[i]);
        if(tp > max)
            max = tp;
        if(tp < min)
            min = tp;
    }
    return new Array(max, min);
}

var  isEmpty=function (str){

    if(str == null || str=="")
        return true;
    return false;
}
/**
 * 按指定长度切割处理字符串
 * @param h 原数据
 * @param size 截取长度
 * @returns {string}
 */
export function splitString (h, size) {
    var string = '';
    //    去除目标字符串中的所有空格
    h = trim_space(h);
    //    获取处理后的字符串长度，计算行数
    var rows = h.length / size;
    if (check_data(h)) {
        return string = '--';
    } else {
        //使用for循环来处理字符
        for (var i = 0; i < rows; i++) {
            string += h.substring(i * size, (i + 1) * size) + '\n';
        }
        //    将剩余未处理的字符追加string的尾部
        // string += h.substring(rows * size, h.length-1);
        return string;
    }
};

//处理时间：时间—> 时间格式字符串
var strFmt = function (str) {
    str = new String(str);
    if (str.length < 2) {
        str = "0" + str;
    } else {
        str = str;
    }
    return str;
}

var dateFormat = function (t) {
    t = new Date(t);
    var year = t.getFullYear();
    var month = strFmt(t.getMonth() + 1);
    var days = strFmt(t.getDate());
    return year + "-" + month + "-" + days;
}

var dataHandles = function (c, fmt) {
    if (check_data(c)) {
        c = fmt;
    }
    return c;
};
/**
 * 为echarts打造 的数字类型字符串处理函数
 * @param e 原始数据
 * @param num1 保留小数位数
 * @param fmtFlag 格式化
 * @returns {number}
 */
var processing_chart = function (e, num1, fmtFlag) {
    var fmt = '-';
    if (fmtFlag != '') {
        fmt = fmtFlag;
    }
    if (check_data(e)) {
        e = dataHandles(e, fmt);
        return e;
    }
    if (isNaN(e)) {
        e = isNaN(fmt) ? dataHandles(e, fmt) : 0;
        console.info('MSG：数据源不是数值类型');
        return e;
    }
    if (isNaN(num1)) {
        e = dataHandles(e, fmt);
        console.info('MSG：精度设置有误，精度num=' + num1);
        return e;
    } else {
        e = Number(e).toFixed(num1);
        return Number(e);
    }
};

export function numberSum (a, b) {

    return Number(a) + Number(b);
}

export function optionXAndX2 (maxNum) {
    var result = [];
    if (Number(maxNum) <= 10000.00) {
        result[0] = "50px";
        result[1] = "50px";
    } else if (Number(maxNum) >= 10000.00 && Number(maxNum) < 100000.00) {
        result[0] = "60px";
        result[1] = "50px";
    } else if (Number(maxNum) >= 100000.00 && Number(maxNum) < 1000000.00) {
        result[0] = "70px";
        result[1] = "50px";
    } else if (Number(maxNum) >= 1000000.00 && Number(maxNum) < 10000000.00) {
        result[0] = "80px";
        result[1] = "50px";
    } else if (Number(maxNum) >= 10000000.00 && Number(maxNum) < 100000000.00) {
        result[0] = "90px";
        result[1] = "50px";
    } else if (Number(maxNum) >= 100000000.00 && Number(maxNum) < 1000000000.00) {
        result[0] = "100px";
        result[1] = "50px";
    } else if (Number(maxNum) >= 1000000000.00 && Number(maxNum) < 10000000000.00) {
        result[0] = "110px";
        result[1] = "50px";
    } else if (Number(maxNum) >= 10000000000.00 && Number(maxNum) < 100000000000.00) {
        result[0] = "120px";
        result[1] = "50px";
    } else if (Number(maxNum) >= 100000000000.00 && Number(maxNum) < 1000000000000.00) {
        result[0] = "130px";
        result[1] = "50px";
    } else if (Number(maxNum) >= 1000000000000.00 && Number(maxNum) < 10000000000000.00) {
        result[0] = "140px";
        result[1] = "50px";
    } else {
        result[0] = "150px";
        result[1] = "50px";
    }

    return result;

}

export function optionX (maxNum) {
    var result = [];
    if (Number(maxNum) <= 10000.00) {
        result[0] = "50px";
    } else if (Number(maxNum) >= 10000.00 && Number(maxNum) < 100000.00) {
        result[0] = "60px";
    } else if (Number(maxNum) >= 100000.00 && Number(maxNum) < 1000000.00) {
        result[0] = "70px";
    } else if (Number(maxNum) >= 1000000.00 && Number(maxNum) < 10000000.00) {
        result[0] = "80px";
    } else if (Number(maxNum) >= 10000000.00 && Number(maxNum) < 100000000.00) {
        result[0] = "90px";
    } else if (Number(maxNum) >= 100000000.00 && Number(maxNum) < 1000000000.00) {
        result[0] = "100px";
    } else if (Number(maxNum) >= 1000000000.00 && Number(maxNum) < 10000000000.00) {
        result[0] = "110px";
    } else if (Number(maxNum) >= 10000000000.00 && Number(maxNum) < 100000000000.00) {
        result[0] = "120px";
    } else if (Number(maxNum) >= 100000000000.00 && Number(maxNum) < 1000000000000.00) {
        result[0] = "130px";
    } else if (Number(maxNum) >= 1000000000000.00 && Number(maxNum) < 10000000000000.00) {
        result[0] = "140px";
    } else {
        result[0] = "150px";
    }
    return result;
}

export function abs (a) {
    if (a >= 0) return a;
    return -a;
}

var sqrt=function(n){
    var s = n / 2; //假设的平方根初值
    while (NotFit(s,n)) {
        s = ((n / s) + s) / 2;
    }
    return s;
}
var NotFit=function( num, n){
    var diff=0.00000000001; //精度
    var r= num*num;
    var d = abs(n - abs(r));
    if(d>diff){
        return true;
    }
    return false;
}

