---
uid: 07
level: 1
chapterNumber: 7
chapterKind: chapter
title: Chapter 7: Coding & Technical Prompts
wordCount: 8459
parentPart: 02-场景-Prompt-模板库
---

# Chapter 7: Coding & Technical Prompts

“AI code generation is like having a senior developer sitting next to you — but only if you speak their language. These 45 technical prompts will help you get production-quality code, not toy snippets.”

## The Technical Prompt Framework

Technical prompts need precision and context.

### The 4-Part Technical Prompt Formula

\[Task\] + [Language/Tool] + \[Constraints\] + [Context/Requirements]

Bad prompt: “Write code for a database connection.”

Good prompt: “Write a Python function using psycopg2 to connect to a PostgreSQL database. Include error handling, connection pooling, and a connection string from environment variables.”

### Why Technical Prompts Need Detail

| Element | Purpose |
| Language | Specific syntax and libraries |
| Framework/version | API differences matter |
| Constraints | Performance, security, patterns |
| Context | Existing codebase integration |

### Common Technical Mistakes

1. No language specified. “Write API code” → could be anything. “Write a FastAPI endpoint in Python” → precise.

2. No version specified. “React code” → React 17 or 19? “React 19 functional component with hooks and TypeScript” → exact.

3. No error handling request. “Write a function that parses JSON” → no defense. “Write a function that parses JSON with proper error handling and typed errors” → production-ready.

## Code Generation (15)

### 166. The Function Generator

"Write a \[language\] function that \[purpose\].
Requirements: \[requirements\].
Error handling: \[specify\].
Tests: [yes/no]."

### 167. The Class Generator

"Write a \[language\] class for \[purpose\].
Include: constructor, key methods, properties, documentation.
Use \[design pattern\] if applicable."

### 168. The Algorithm Generator

"Write a \[algorithm type\] algorithm in \[language\] for \[problem\].
Optimize for [time/space] complexity.
Include comments and test cases."

### 169. The API Endpoint Generator

"Write a \[HTTP method\] endpoint in \[framework\] for \[purpose\].
Include: route, request/response models, authentication,
error responses."

### 170. The Database Query Generator

"Write a SQL query for \[database\] that \[purpose\].
Tables: \[list\]. Requirements: \[details\].
Optimize for performance."

### 171. The Configuration Generator

"Generate a \[config file type\] file for \[technology\]
with these settings: \[settings\].
Include comments explaining each setting."

### 172. The Script Generator

"Write a \[language\] script that \[purpose\].
Input: \[source\]. Output: \[destination\].
Error handling: \[specify\]."

### 173. The Data Structure Generator

"Create a \[data structure\] in \[language\] for \[purpose\].
Include: definition, key operations, time complexity,
example usage."

### 174. The Dockerfile Generator

"Write a Dockerfile for \[application type\] using \[base image\].
Include: dependencies, build steps, runtime config,
health checks, non-root user."

### 175. The CI/CD Pipeline Generator

"Create a GitHub Actions workflow for \[project type\].
Include: build, test, deploy steps.
Environment: \[specify\]. Secrets to wire: \[list\]."

### 176. The Regex Generator

"Write a regex pattern for \[language\] that \[purpose\].
Input format: \[describe\].
Edge cases: \[list\]. Include test strings."

### 177. The Unit Test Generator

"Write unit tests for [function/class] in \[language\]
using \[testing framework\].
Cover: happy path, edge cases, error cases.
Target coverage: \[percent\]."

### 178. The Migration Script Generator

"Write a database migration script for \[database\] that \[purpose\].
Include: up migration, down migration, rollback plan,
and a dry-run check."

### 179. The API Client Generator

"Write an API client in \[language\] for \[API\].
Include: authentication, request methods,
error handling, rate limiting, retries with backoff."

### 180. The CLI Tool Generator

"Create a CLI tool in \[language\] that \[purpose\].
Include: command structure, options/flags,
help text, error handling, shell completion."

## Code Explanation (10)

### 181. The Line-by-Line Explanation

"Explain this code line by line: \[code\].
Assume the reader knows \[basic concepts\]
but not \[advanced concepts\]."

### 182. The Architecture Overview

"Explain the architecture of this codebase.
Include: main components, data flow, design patterns,
strengths/weaknesses."

### 183. The Performance Analysis

"Analyze the performance of this code.
Identify: time complexity, space complexity,
bottlenecks, optimization opportunities."

### 184. The Security Review

"Review this code for security vulnerabilities.
Identify: common vulnerabilities, input validation issues,
authentication/authorization gaps.
Reference OWASP Top 10 where applicable."

### 185. The Best-Practices Assessment

"Assess this code against \[language\] best practices.
Include: what's good, what could be improved,
specific recommendations with code examples."

### 186. The Legacy Code Analysis

"Analyze this legacy code for refactoring.
Include: current behavior, technical debt,
refactoring priorities, test strategy."

### 187. The Debugging Assistant

"This code is producing \[unexpected behavior\].
Identify the likely cause and provide a fix.
Code: \[code\]. Error: \[stack trace\]."

### 188. The Dependency Analysis

"Analyze these dependencies for \[project\].
Include: purpose of each, version compatibility,
security vulnerabilities, alternatives."

### 189. The Code Review Summary

"Review this pull request.
Include: overall assessment, specific feedback,
approval status (approve / request changes),
suggested improvements with line references."

### 190. The Technical Debt Assessment

"Assess the technical debt in this codebase.
Include: categories of debt, impact on development,
priority fixes, timeline estimate."

## Python-Specific (5)

### 191. The Pandas Data Analysis

"Write Python code using pandas to \[purpose\]
with this DataFrame structure: \[describe\].
Include error handling and documentation."

### 192. The FastAPI Endpoint

"Write a FastAPI endpoint for \[purpose\].
Include: Pydantic request/response models,
authentication dependency, error handling,
OpenAPI-friendly docstrings."

### 193. The asyncio Function

"Write an async Python function that \[purpose\].
Include: async/await, error handling,
timeout, and example usage with asyncio.run."

### 194. The Dataclass Generator

"Create a Python dataclass for \[purpose\]
with these fields: \[list\].
Include: type hints, defaults, validation,
to_dict / from_dict methods."

### 195. The Context Manager

"Write a Python context manager for \[purpose\].
Include: __enter__ and __exit__, error handling,
and example usage."

## JavaScript / TypeScript (5)

### 196. The React Component

"Write a React functional component for \[purpose\] in TypeScript.
Include: props interface, state management,
effects, error handling, and basic accessibility."

### 197. The Node.js API

"Write a Node.js Express endpoint for \[purpose\].
Include: route definition, request validation with Zod,
error handling, structured logging, response formatting."

### 198. The TypeScript Utility Type

"Create a TypeScript utility type that \[purpose\].
Include: type definition, example usage, edge cases."

### 199. The Async Function

"Write async JavaScript that \[purpose\].
Include: error handling, timeout via AbortController,
and optional progress callbacks."

### 200. The ESLint Configuration

"Create an ESLint flat config for a \[project type\] project.
Include: rules, plugins, environment settings,
and editor integration notes."

## SQL & Database (5)

### 201. The Complex Query

"Write a SQL query for \[database\] that \[purpose\].
Tables: \[list\]. Joins: \[specify\]. Conditions: \[details\].
Optimize for performance and include an EXPLAIN plan note."

### 202. The Index Strategy

"Design indexes for table \[table_name\] with these queries:
\[list\]. Include: index types, column order, coverage,
and trade-offs."

### 203. The Transaction

"Write a SQL transaction for \[purpose\] in \[database\].
Include: BEGIN, operations, COMMIT/ROLLBACK, error handling,
and appropriate isolation level."

### 204. The Migration

"Write a database migration for \[change\] in \[database\].
Include: up migration, down migration, data validation,
and a backout plan."

### 205. The View

"Create a SQL view for \[purpose\] that \[requirements\].
Include: SELECT statement, joins, filters,
and documentation of refresh frequency."

## DevOps & Infrastructure (5)

### 206. The Terraform Module

"Write a Terraform module for \[resource\] with variables: \[list\].
Include: resource definition, variables, outputs,
and README documentation."

### 207. The Kubernetes Manifest

"Write a Kubernetes deployment manifest for \[application\].
Include: Deployment, Service, ConfigMap,
health checks, resource limits,
and a minimal securityContext."

### 208. The AWS Lambda

"Write an AWS Lambda function in \[language\] for \[purpose\].
Include: handler function, event processing,
error handling, IAM permissions note."

### 209. The Monitoring Alert

"Create a CloudWatch alert for \[metric\] with \[threshold\].
Include: metric definition, threshold, actions,
notification configuration, and a runbook link."

### 210. The Security Group

"Create a security group configuration for \[application\]
with these requirements: \[list\].
Include: inbound rules, outbound rules, and documentation."

## Chapter Summary

Technical prompts require more precision than general prompts, but the payoff is production-quality code and configurations.

1. Always specify language and version.
2. Include error-handling requirements.
3. Provide context about the existing codebase.
4. Ask for documentation and tests.

Next: 60 prompts for image generation with Midjourney, DALL-E, Stable Diffusion, and the current crop of 2026 image models.
