import { createRequire } from 'module'

const require = createRequire(import.meta.url)

require('babel-register')({
  babelrc: false,
  presets: [['env', { modules: 'commonjs', targets: { node: '14' } }], 'stage-2'],
  plugins: ['transform-runtime'],
  extensions: ['.js']
})

export function loadVmSource(relativePath) {
  return require(relativePath)
}
