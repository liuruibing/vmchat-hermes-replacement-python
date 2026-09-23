module.exports = {
  devServer: { disableHostCheck: true },
  NODE_ENV: '"development"',
  ENV_CONFIG: '"dev"',
  // BASE_API: '"http://datadriver.tpddns.cn:8000/cmbblfof/"'
  // BASE_API: '"http://10.50.25.167:8005/pfl/"'
  // BASE_API: '"/pfl"'
  // BASE_API: '"http://datadriver.tpddns.cn:8000/nfof"'
  // BASE_API: '"http://datadriver.tpddns.cn:8001/fof"'
  // BASE_API: '"http://192.168.10.133:8001/fof"'
  // BASE_API: '"http://192.168.1.203:8010/ddetlrest"'
  // BASE_API: '"http://http://vip.datadriver.com.cn:8010/ddetlrest"'
  // BASE_API: '"http://192.168.10.123:8087/ddetl"'
  // BASE_API: '"http://192.168.10.248:8001/cmbblfof"'
  // BASE_API: '"http://vip.datadriver.com.cn:9060/pfomrest/"'
  //  BASE_API: '"http://vip.datadriver.com.cn:9600/pfom/"'
  //  BASE_API: '"http://192.168.1.12:8090/pfom/"',
  // BASE_API: '"http://192.168.137.1:8090/pfom/"',
  // BASE_API: '"http://192.168.10.134:8090/pfom/"',
  //BASE_API: '"http://192.168.10.219:8090/pfom/"'
  // BASE_API: '"http://192.168.10.243:9600/pfom/"'
  //  BASE_API: '"http://192.168.10.24:9600/pfom/"'
  // BASE_API: '"http://192.168.10.247:8090/pfom/"'
  // BASE_API: '"http://localhost/pfom/"'
  // BASE_API: '"http://192.168.137.240:8090/pfom/"'
  // BASE_API: '"http://192.168.10.119:8090/pfom/"'
  BASE_API: '"/pfl"',
  // 由启动前端时的 HERMES_API_KEY 注入，避免把本地 Hermes 密钥提交到代码库
  HERMES_API_KEY: JSON.stringify(process.env.HERMES_API_KEY || '')
}
