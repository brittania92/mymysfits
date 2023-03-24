# vue

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin) to make the TypeScript language service aware of `.vue` types.

If the standalone TypeScript plugin doesn't feel fast enough to you, Volar has also implemented a [Take Over Mode](https://github.com/johnsoncodehk/volar/discussions/471#discussioncomment-1361669) that is more performant. You can enable it by the following steps:

1. Disable the built-in TypeScript Extension
    1) Run `Extensions: Show Built-in Extensions` from VSCode's command palette
    2) Find `TypeScript and JavaScript Language Features`, right click and select `Disable (Workspace)`
2. Reload the VSCode window by running `Developer: Reload Window` from the command palette.

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Run Unit Tests with [Vitest](https://vitest.dev/)

```sh
npm run test:unit
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```

## Connections and permissions

This blueprint requires a custom development role.  To create one, click "Add an existing IAM role" from the add IAM role options. The IAM role needs to contain the CodeCatalyst trust policy, as well as the following permissions:

```
{
  "Version": "2012-10-17",
  "Statement": [
      {
          "Effect": "Allow",
          "Action": [
              "cloudformation:*",
              "ecr:*",
              "ssm:*",
              "s3:*",
              "codeguru-reviewer:*",
              "iam:Get*",
              "iam:PassRole",
              "iam:CreateRole",
              "iam:DeleteRole",
              "iam:TagRole",
              "iam:UpdateRole",
              "iam:AttachRolePolicy",
              "iam:DetachRolePolicy",
              "iam:PutRolePolicy",
              "iam:CreatePolicy",
              "iam:DeletePolicy",
              "iam:CreatePolicyVersion",
              "iam:CreateServiceLinkedRole",
              "iam:DeletePolicyVersion",
              "iam:PutRolePermissionsBoundary",
              "iam:DeleteRolePermissionsBoundary",
              "sts:AssumeRole",
              "sts:GetCallerIdentity"
          ],
          "Resource": "*"
      }
  ]
}
```

The IAM roles also require the Amazon CodeCatalyst service principals `codecatalyst.amazonaws.com` and `codecatalyst-runner.amazonaws.com`.

### Required IAM role trust policy:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "Service": [
                    "codecatalyst.amazonaws.com",
                    "codecatalyst-runner.amazonaws.com"
                ]
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```