import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Locale;
import java.util.Map;

public class Exercise7 {
    public static void main(String[] args) throws IOException {
        Path input = args.length > 0 && !args[0].equals("--summary")
                ? Path.of(args[0]) : CandidateData.DEFAULT_FILE;
        Path output = args.length > 1 && !args[1].equals("--summary")
                ? Path.of(args[1]) : Path.of("groups");
        CandidateData data = CandidateData.read(input);
        if (!Arrays.asList(args).contains("--summary")) {
            data.display();
        }
        Map<String, ArrayList<Candidate>> groups = CandidateStatistics.byGroup(data.candidates());
        for (String group : List.of("A", "B", "C", "D")) {
            groups.computeIfAbsent(group, key -> new ArrayList<>());
        }
        Files.createDirectories(output);
        int exported = 0;
        for (Map.Entry<String, ArrayList<Candidate>> entry : groups.entrySet()) {
            List<Candidate> members = entry.getValue();
            ArrayList<List<String>> rows = new ArrayList<>();
            rows.add(data.header());
            for (Candidate candidate : members) {
                rows.add(candidate.row());
            }
            int width = data.header().size();
            rows.add(summaryRow(width, "Summary - total students", Integer.toString(members.size())));
            rows.add(summaryRow(width, "Summary - male (%)", percent(members, "male")));
            rows.add(summaryRow(width, "Summary - female (%)", percent(members, "female")));
            Path file = output.resolve("group" + entry.getKey() + ".csv");
            Csv.write(file, rows);
            CandidateStatistics.printGenderSummary("Group " + entry.getKey(), members);
            System.out.println("Wrote " + file);
            System.out.println();
            exported += members.size();
        }
        System.out.println("Exported " + exported + " candidates to " + groups.size() + " group files.");
    }

    private static List<String> summaryRow(int width, String label, String value) {
        ArrayList<String> row = new ArrayList<>(Collections.nCopies(width, ""));
        row.set(0, label);
        row.set(1, value);
        return row;
    }

    private static String percent(List<Candidate> candidates, String gender) {
        return String.format(Locale.ROOT, "%.2f%%", CandidateStatistics.percentage(
                CandidateStatistics.countGender(candidates, gender), candidates.size()));
    }
}
