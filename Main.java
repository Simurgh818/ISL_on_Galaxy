import com.sun.xml.internal.fastinfoset.util.CharArray;
import org.omg.Messaging.SYNC_WITH_TRANSPORT;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class Main {
    public static void main (String [] args) throws  Exception {
        try {
            File file = new File("/home/sinadabiri/Fiji.app/tutorials/ud282/src/movies.txt");
            Scanner scanner = new Scanner(file);
            String movies =  " " ;
            String [] ArrayMovies = new String[24];
            int letters = 0;
            String MoviesLetters = " ";
            boolean TheyWon = false;

            while (scanner.hasNextLine()){
                String line = scanner.nextLine();

                movies = line;
//                System.out.println(movies+ "\n");
                ArrayMovies = line.split(", ");

//                letters = line.split(", ");

            }
            int NumberOfMovies = ArrayMovies.length;

            System.out.println("There are " + NumberOfMovies + " movies to guess from.");

            int number = (int) (Math.random()*22)+1;
            System.out.println(ArrayMovies[number]);
            System.out.println("Please type in the letter for the movie: ");

//            System.out.println(guess + "\n");
//            for (int i=0; i< NumberOfMovies; i++) {
//               if (ArrayMovies[i].contains(guess)) {
//                    letters = guess.replace(" ", "").length();
//                    System.out.println(guess + " : " + letters+ " letters long");
//                    for (int j = 0; j < letters; j++) {
//                        System.out.print("-");
//                    }
//
//                }
////
//            }
//            String GuessInProgress = "";
            char [] GuessInProgress = new char[ArrayMovies[number].length()];
//            StringBuilder GIP = new StringBuilder(GuessInProgress);
            for (int j = 0; j < ArrayMovies[number].length(); j++) {
                GuessInProgress[j] = '-';
            }
            System.out.println(GuessInProgress);
            for (int i =10; i>0; i--){
                System.out.println("Try to guess a letter. You have " + i + " trials left!");
                Scanner scanner1 = new Scanner(System.in);
                String guess = scanner1.next();
//                letters = guess.replace(" ", "").length();
                char[] CharArrayMovies = ArrayMovies[number].toCharArray();
                char[] CharGuess = guess.toCharArray();
//                System.out.println(CharArrayMovies);

                for (int j = 0; j < ArrayMovies[number].length(); j++) {
//                    System.out.print(CharArrayMovies[j]);
                    if (CharGuess[0] == CharArrayMovies[j]) {
                        GuessInProgress[j] = CharGuess[0];
                    }
//                    else {
//                        GIP.replace(0, j,"-");
//                    }
                }
                System.out.println(GuessInProgress);
//                    TheyWon = true;
//                    break;
//                } else {
//
//                    if ( guess>number) {
//                        System.out.println("It is smaller than " + guess);
//                    } else {
//                        System.out.println("It is bigger than " + guess);
//                    }
//
//                }
//
//            }
//            if (TheyWon) {
//                System.out.println("Great Job, you WON!");
//            }else {
//                System.out.println("Game Over, you Lost! The number is " + number);
            }
        System.out.println("\n");
        } catch (FileNotFoundException e){
                    System.out.println("File Missing!");
            } }
}

