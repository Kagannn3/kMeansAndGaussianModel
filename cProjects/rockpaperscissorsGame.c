#include<stdio.h>  // for general 
#include<stdlib.h> // for rand() function
#include<time.h>  // for time() function 
#include<string.h> // for strcmp() function 
//
int main(){
    int random_number;
    int my_score=0;
    char user_choice[10];  
    char *exit_sen; // *exit_sen means that exit will hold the memory address of a character 
    exit_sen= (char*)malloc(5*sizeof(char)); // allocating memory for a string of up to 4 characters, the last character is null(\0)
    sprintf(exit_sen,"exit"); // assign a value to the string 
    srand(time(NULL));  // seed the random number generator
    // when I each run the program, random number generator generate any random number and will use just 1 time it 
    random_number=rand()%3;  // random number will be any number between 0-2

    char strings[][20]={"rock","paper","scissors"}; // each strings can have 20 characters 
    printf("Computer decided on the its choice:\n");
    printf("Please enter your choice between rock,paper,scissors:\n");
    while(1){ // infinite loop
       scanf("%s", user_choice);
       if(strcmp(user_choice,exit_sen)==0)
          break;
       printf("Computer chose %s ",strings[random_number]);
       if(strcmp(user_choice,strings[random_number])==0)  // strcmp function is comparing the 2 strings
        printf("\nDraw");
       else{
        if((strcmp(user_choice,strings[0])==0 && random_number==1)||
        (strcmp(user_choice,strings[1])==0 &&random_number==2)||
        (strcmp(user_choice,strings[2])==0 &&random_number==0)){
            printf("\nYou lose");my_score--;}
        else 
            printf("\nYou won");my_score++;
       }
    }
    printf("Game over\n");
    printf("The score is:\n");
    printf("My score is: %d\n", my_score);
    return 0; 
}