# RAG Knowledge Base

## What is RAG?

Retrieval-Augmented Generation (RAG) is a method that combines information retrieval with language generation. A RAG system retrieves relevant information from a collection of data and provides that information as context to a language model when generating an answer.

## Why is RAG useful?

A language model's knowledge may not contain a user's private documents or information that was added after the model's training. RAG can allow a system to retrieve relevant information from an external knowledge source and use that information when answering a question.

RAG can help improve the relevance and factual grounding of answers, but it does not guarantee that every generated answer will be correct.

## Basic RAG flow

A simple RAG process can be described as:

1. The user asks a question.
2. The system searches a knowledge source for relevant information.
3. Relevant retrieved information is provided to the language model as context.
4. The language model generates an answer using the question and retrieved context.

## Retrieval

Retrieval means finding information that is relevant to a user's question from a collection of stored information.

A retrieval system may return relevant documents, passages, or chunks of information.

## Augmentation

In RAG, augmentation means adding the retrieved information to the context provided to the language model.

## Generation

Generation is the process where the language model produces an answer based on the user's question and the available context.

## Important limitation

RAG does not automatically make every answer correct. Problems can occur if the system retrieves irrelevant, incomplete, outdated, or incorrect information, or if the language model incorrectly uses the retrieved information.

## Example

Suppose a company has a document containing its leave policy. A user asks, "How many days of annual leave can I take?"

A RAG system can retrieve the relevant part of the company's leave-policy document and provide it as context to the language model. The model can then generate an answer based on that retrieved information.