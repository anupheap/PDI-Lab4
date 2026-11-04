import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.TreeMap;
import java.util.function.ToDoubleFunction;

public final class CandidateStatistics {
    private CandidateStatistics() { }

    public static long countGender(List<Candidate> candidates, String gender) {
        return candidates.stream().filter(candidate -> candidate.gender().equals(gender)).count();
    }

    public static double percentage(long count, int total) {
        return total == 0 ? 0.0 : 100.0 * count / total;
    }

    public static ArrayList<Candidate> averageAtLeast(List<Candidate> candidates, double minimum) {
        ArrayList<Candidate> result = new ArrayList<>();
        for (Candidate candidate : candidates) {
            if (candidate.average() >= minimum) {
                result.add(candidate);
            }
        }
        return result;
    }

    public static long subjectAtLeast(List<Candidate> candidates,
                                      ToDoubleFunction<Candidate> score, double minimum) {
        return candidates.stream().filter(candidate -> score.applyAsDouble(candidate) >= minimum).count();
    }

    public static long allSubjectsAtLeast(List<Candidate> candidates, double minimum) {
        return candidates.stream().filter(candidate -> candidate.math() >= minimum
                && candidate.english() >= minimum && candidate.computer() >= minimum).count();
    }

    public static Map<String, ArrayList<Candidate>> byGroup(List<Candidate> candidates) {
        Map<String, ArrayList<Candidate>> groups = new TreeMap<>();
        for (Candidate candidate : candidates) {
            groups.computeIfAbsent(candidate.group(), key -> new ArrayList<>()).add(candidate);
        }
        return groups;
    }

    public static void printGenderSummary(String title, List<Candidate> candidates) {
        System.out.println(title);
        System.out.println("Total candidates: " + candidates.size());
        long male = countGender(candidates, "male");
        long female = countGender(candidates, "female");
        System.out.printf(Locale.ROOT, "Male candidates: %d (%.2f%%)%n", male,
                percentage(male, candidates.size()));
        System.out.printf(Locale.ROOT, "Female candidates: %d (%.2f%%)%n%n", female,
                percentage(female, candidates.size()));
    }
}
