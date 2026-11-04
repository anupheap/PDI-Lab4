import java.io.IOException;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

public record CandidateData(List<String> header, ArrayList<Candidate> candidates) {
    public static final Path DEFAULT_FILE = Path.of("data", "CandidatePerformanceTest.csv");
    private static final List<String> REQUIRED =
            List.of("id", "gender", "group", "math", "english", "computer", "average");

    public static CandidateData read(Path file) throws IOException {
        ArrayList<List<String>> rows = Csv.read(file);
        Map<String, Integer> columns = new HashMap<>();
        int headerIndex = -1;
        for (int i = 0; i < rows.size(); i++) {
            columns.clear();
            List<String> row = rows.get(i);
            for (int j = 0; j < row.size(); j++) {
                columns.put(normalize(row.get(j)), j);
            }
            if (columns.keySet().containsAll(REQUIRED)) {
                headerIndex = i;
                break;
            }
        }
        if (headerIndex < 0) {
            throw new IOException("Missing candidate header; required columns: " + REQUIRED);
        }
        List<String> header = List.copyOf(rows.get(headerIndex));
        ArrayList<Candidate> candidates = new ArrayList<>();
        for (int i = headerIndex + 1; i < rows.size(); i++) {
            List<String> row = rows.get(i);
            if (row.stream().allMatch(String::isBlank)) {
                continue;
            }
            try {
                if (row.size() != header.size()) {
                    throw new IllegalArgumentException("Expected " + header.size() + " fields");
                }
                String gender = row.get(columns.get("gender")).trim().toLowerCase(Locale.ROOT);
                if (!gender.equals("male") && !gender.equals("female")) {
                    throw new IllegalArgumentException("Unknown gender: " + gender);
                }
                String group = row.get(columns.get("group")).trim().toUpperCase(Locale.ROOT);
                if (group.matches("GROUP\\s+[A-Z]")) {
                    group = group.substring(group.length() - 1);
                }
                if (!group.matches("[A-Z]")) {
                    throw new IllegalArgumentException("Invalid group: " + group);
                }
                candidates.add(new Candidate(row, gender, group,
                        score(row, columns, "math"), score(row, columns, "english"),
                        score(row, columns, "computer"), score(row, columns, "average")));
            } catch (IllegalArgumentException exception) {
                throw new IOException("Invalid candidate CSV record " + (i + 1) + ": "
                        + exception.getMessage(), exception);
            }
        }
        return new CandidateData(header, candidates);
    }

    private static String normalize(String value) {
        return value.trim().toLowerCase(Locale.ROOT).replaceAll("[^a-z0-9]", "");
    }

    private static double score(List<String> row, Map<String, Integer> columns, String name) {
        double value = Double.parseDouble(row.get(columns.get(name)).trim());
        if (!Double.isFinite(value) || value < 0 || value > 100) {
            throw new IllegalArgumentException(name + " score must be between 0 and 100");
        }
        return value;
    }

    public void display() {
        System.out.println(String.join(" | ", header).replace('\r', ' ').replace('\n', ' '));
        for (Candidate candidate : candidates) {
            System.out.println(String.join(" | ", candidate.row()));
        }
        System.out.println();
    }
}
