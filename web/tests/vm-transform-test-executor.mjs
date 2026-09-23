export async function executeTransformForTest(transformSource, responses) {
  const transform = Function('"use strict"; return (' + transformSource + ');')()
  return transform(JSON.parse(JSON.stringify(responses || {})))
}
