
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

// I'm sure I'm missing something, or could combine.
// But onward.
enum token_type
{
    KEYWORD,
    NUMBER,
    IDENTIFIER,
    OPERATOR,
    TOKEN_EOL,
    TOKEN_EOF
};

const char *keywords[] = {
    "LET",
    "FOR",
    "TO",
    "IF",
    "ELSE",
    "WHILE",
    "GOTO",
    "PRINT",
    "NEXT"};

const char operators[] = {'=', '+', '-', '>', '<'};

// Each token will have a type and a value. For tokens with no value we canjust ignore not read it.
// And as our source files will be small, I'll implement our tokens as a linked list as preformance isn't a concern.
typedef struct Token
{
    enum token_type type;
    char *value;
    struct Token *next;

} Token;

int is_keyword(const char *phrase)
{
    for (size_t i = 0; i < sizeof(keywords) / sizeof(char *); i++)
    {
        if (strcmp(phrase, keywords[i]) == 0)
        {
            return 1;
        }
    }
    return 0;
}

int is_operator(const char input)
{
    for (size_t i = 0; i < sizeof(operators) / sizeof(char); i++)
    {
        if (input == operators[i])
        {
            return 1;
        }
    }
    return 0;
}

/*
    So the plan is to scan the source into tokens, and return an array of tokens. Simple enough...
*/
Token *tokenize(const char *current_char)
{
    Token *head = NULL;
    Token *tail = NULL;

    while (*current_char != '\0')
    {
        Token *new_token = malloc(sizeof(Token));

        while (isspace(*current_char)) // skip whitespace
        {
            current_char++;
        }

        if (*current_char == '\n')
        {
            new_token->type = TOKEN_EOL;
            current_char++;
        }
        else if (isdigit(*current_char)) // handle numbers
        {
            // Numbers can either by line numbers as read by the interpreter, or number literals.
            // For now we'll scan the number up until 5 chars long. Doesn't really matter right now.
            char num[5];
            int i = 0;
            while (isdigit(*current_char))
            {
                num[i++] = *current_char++;
            }
            num[i] = '\0';
            new_token->type = NUMBER;
            new_token->value = strdup(num);
        }
        else if (isalpha(*current_char)) // identifier or keyword
        {
            char buffer[16]; // assuming identifier or keyword will not exceed this size
            int i = 0;
            while (isalnum(*current_char))
            { // identifiers can include numbers but cannot start with them
                buffer[i++] = *current_char++;
            }
            buffer[i] = '\0';

            if (strcmp(buffer, "END") == 0)
            {
                new_token->type = TOKEN_EOF;
            }
            else if (is_keyword(buffer))
            {
                new_token->type = KEYWORD;
            }
            else
            {
                new_token->type = IDENTIFIER;
            }
            new_token->value = strdup(buffer);
        }
        else if (is_operator(*current_char)) // scan operators
        {
            char buffer[3];
            buffer[2] = '\0';
            int i = 0;
            while (is_operator(*current_char))
            {
                buffer[i++] = *current_char++;
            }

            buffer[i] = '\0';
            new_token->type = OPERATOR;
            new_token->value = strdup(buffer);
        }

        if (tail == NULL)
        {
            head = new_token;
            tail = new_token;
        }
        else
        {
            tail->next = new_token;
            tail = new_token;
        }
    }

    // Add EOF token at the end of the list
    Token *eof_token = malloc(sizeof(Token));
    eof_token->type = TOKEN_EOF;
    eof_token->value = NULL;
    eof_token->next = NULL;

    if (tail == NULL)
    {
        head = eof_token;
    }
    else
    {
        tail->next = eof_token;
    }

    return head;
}
