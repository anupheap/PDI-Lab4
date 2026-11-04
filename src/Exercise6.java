import java.io.IOException;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Map;

public class Exercise6 {
    public static void main(String[] args) throws IOException {
        Path file = args.length > 0 && !args[0].equals("--summary")
                ? Path.of(args[0]) : CandidateData.DEFAULT_FILE;
        CandidateData data = CandidateData.read(file);
        if (!Arrays.asList(args).contains("--summary")) {
            data.display();
        }
        ArrayList<Candidate> candidates = data.candidates();
        CandidateStatistics.printGenderSummary("All candidates", candidates);
        CandidateStatistics.printGenderSummary("Average score >= 90",
                CandidateStatistics.averageAtLeast(candidates, 90));
        System.out.println("Math score >= 85: "
                + CandidateStatistics.subjectAtLeast(candidates, Candidate::math, 85));
        System.out.println("English score >= 85: "
                + CandidateStatistics.subjectAtLeast(candidates, Candidate::english, 85));
        System.out.println("Computer score >= 85: "
                + CandidateStatistics.subjectAtLeast(candidates, Candidate::computer, 85));
        System.out.println("All three subjects >= 85: "
                + CandidateStatistics.allSubjectsAtLeast(candidates, 85));
        System.out.println();
        for (Map.Entry<String, ArrayList<Candidate>> group
                : CandidateStatistics.byGroup(candidates).entrySet()) {
            CandidateStatistics.printGenderSummary("Group " + group.getKey(), group.getValue());
        }
    }
}
