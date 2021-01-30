module.exports = {
  plugins: [
    "vue"
  ],
  extends: [
    "eslint:recommended",
    'plugin:vue/essential',
    '@vue/typescript/recommended'
  ],
  parserOptions: {
    ecmaVersion: 2020
  },
  rules: {
    "comma-spacing": 2,
    "computed-property-spacing": 2,
    "func-call-spacing": [2, "never"],
    "indent": [2, 2, { "SwitchCase": 1 }],
    "key-spacing": 2,
    "keyword-spacing": 2,
    "no-console": 0,
    "no-extra-parens": 1,
    "no-multi-spaces": 2,
    "no-multiple-empty-lines": [2, { "max": 1 }],
    "no-unneeded-ternary": 2,
    "no-var": 2,
    "quotes": [2, "double"],
    "semi": [2, "never"],
    "space-in-parens": [2, "never"],
    "vue/no-v-html": 0,
    "vue/html-closing-bracket-newline": [2, { "multiline": "never" }],
    "vue/max-attributes-per-line": ["error", {
      "singleline": 80,
      "multiline": {
        "max": 1,
        "allowFirstLine": false
      }
    }],
    "vue/singleline-html-element-content-newline": 0
  }
}
