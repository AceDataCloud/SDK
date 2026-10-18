"""Limited offline expression evaluation; this is not the Make IML runtime."""

import json
import subprocess

EVALUATOR = r"""
const vm = require('node:vm');
let input = '';
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
  const { communication, body, taskId } = JSON.parse(input);
  const get = (value, path) => path.split('.').reduce((v, key) =>
    v?.[Array.isArray(v) && /^\d+$/.test(key) ? Number(key) - 1 : key], value);
  const context = {
    body, parameters: { task_id: taskId }, temp: {}, emptyarray: [],
    get, keys: value => Object.keys(value ?? {}),
    ifempty: (v, fallback) => v === undefined || v === null || v === '' ? fallback : v,
    choose: (condition, yes, no) => condition ? yes : no,
    length: value => value?.length ?? 0,
    contains: (values, value) => values.includes(value),
  };
  const evaluate = text => typeof text !== 'string' || !text.startsWith('{{')
    ? text : vm.runInNewContext(text.slice(2, -2).replace(/\bif\(/g, 'choose('), context);
  if (!evaluate(communication.response.valid.condition)) {
    process.stdout.write(JSON.stringify({ rejected: true })); return;
  }
  for (const [key, expression] of Object.entries(communication.response.temp))
    context.temp[key] = evaluate(expression);
  process.stdout.write(JSON.stringify(Object.fromEntries(
    Object.entries(communication.response.output).map(([key, expr]) => [key, evaluate(expr)]))));
});
"""


def evaluate_task(communication, body, task_id="same-task"):
    result = subprocess.run(
        ["node", "-e", EVALUATOR],
        input=json.dumps(
            {"communication": communication, "body": body, "taskId": task_id}
        ),
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)
