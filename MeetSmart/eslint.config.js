import js from '@eslint/js';
import globals from 'globals';
import reactHooks from 'eslint-plugin-react-hooks';
import reactRefresh from 'eslint-plugin-react-refresh';
import { ESLint } from 'eslint';
import tseslint from '@typescript-eslint/eslint-plugin';
import tsParser from '@typescript-eslint/parser';

export default [
    {
        ignores: ['dist'],
    },
    {
        extends: [
            'eslint:recommended',
            'plugin:@typescript-eslint/recommended',
        ],
        files: ['**/*.{ts,tsx}'],
        parser: tsParser,
        parserOptions: {
            ecmaVersion: 2020,
            sourceType: 'module',
        },
        env: {
            browser: true,
            es2020: true,
        },
        globals: globals.browser,
        plugins: {
            'react-hooks': reactHooks,
            'react-refresh': reactRefresh,
            '@typescript-eslint': tseslint,
        },
        rules: {
            ...reactHooks.configs.recommended.rules,
            'react-refresh/only-export-components': [
                'warn',
                { allowConstantExport: true },
            ],
        },
    },
];