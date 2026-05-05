# TypeScript guidelines

Remember to read the general guidelines in the main README first!

Use TypeScript over plain JavaScript - the type system catches bugs early
and makes refactoring safer.

## Use Node.js

Use an [LTS][nodelts] release that still has a long support window ahead,
rather than one nearing end-of-life.

[nodelts]: https://nodejs.org/en/about/previous-releases

## Use [pnpm][pnpm]

Stricter dependency resolver than npm or yarn. Commit the lockfile and have
CI install with `pnpm install --frozen-lockfile`.

[pnpm]: https://pnpm.io/

## Strict type checking

Set `"strict": true` in `tsconfig.json`. Use `any` only when you absolutely
have to (e.g. crossing a module-federation boundary the compiler can't
statically see through), not to silence errors you could otherwise fix.

## Use [ESLint][eslint]

Use the modern flat config (`eslint.config.js`) with `typescript-eslint` and
for React projects, `eslint-plugin-react-hooks`. Configure import ordering so
diffs stay tidy.

[eslint]: https://eslint.org/

## Use [Prettier][prettier]

It auto-formats your code to a common standard.

[prettier]: https://prettier.io/

## Code-quality checks

Use the [config-ci-library][cilib] pre-commit templates and run them locally
with [prek][prek]. CI should run the same pre-commit checks using the action available.

[cilib]: https://github.com/pvarki/config-ci-library
[prek]: https://github.com/j178/prek
