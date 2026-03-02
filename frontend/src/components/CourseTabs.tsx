import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { CheckCircle2, Circle, Lock } from "lucide-react";

const weeklyModules = [
  { week: 1, title: "Foundations of Statistical Learning", status: "completed" },
  { week: 2, title: "Linear Models & Regularization", status: "completed" },
  { week: 3, title: "Kernel Methods & SVMs", status: "completed" },
  { week: 4, title: "Neural Network Architectures", status: "current" },
  { week: 5, title: "Convolutional Neural Networks", status: "locked" },
  { week: 6, title: "Recurrent Networks & Attention", status: "locked" },
  { week: 7, title: "Generative Models", status: "locked" },
  { week: 8, title: "Reinforcement Learning", status: "locked" },
];

const CourseTabs = () => {
  const [activeTab, setActiveTab] = useState("overview");

  return (
    <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
      <TabsList className="w-full justify-start gap-1 rounded-lg bg-muted p-1 h-auto">
        {["Overview", "Weekly Modules", "Grading Policy", "Certification"].map((tab) => (
          <TabsTrigger
            key={tab}
            value={tab.toLowerCase().replace(" ", "-")}
            className="rounded-md px-4 py-2 text-sm font-medium data-[state=active]:bg-card data-[state=active]:shadow-card data-[state=active]:text-foreground text-muted-foreground transition-all"
          >
            {tab}
          </TabsTrigger>
        ))}
      </TabsList>

      <TabsContent value="overview" className="mt-5 space-y-4">
        <div className="rounded-lg border bg-card p-5 shadow-card">
          <h3 className="text-base font-semibold text-foreground mb-3 font-serif">About This Course</h3>
          <p className="text-sm leading-relaxed text-muted-foreground">
            This graduate-level course covers the theoretical foundations and practical applications of modern machine learning. 
            Topics include supervised and unsupervised learning, deep neural networks, generative models, and reinforcement learning. 
            Students will gain hands-on experience through weekly assignments and a capstone project.
          </p>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div className="rounded-lg border bg-card p-5 shadow-card">
            <h4 className="text-sm font-semibold text-foreground mb-2">Prerequisites</h4>
            <ul className="space-y-1.5 text-sm text-muted-foreground">
              <li>Linear Algebra</li>
              <li>Probability & Statistics</li>
              <li>Python Programming</li>
            </ul>
          </div>
          <div className="rounded-lg border bg-card p-5 shadow-card">
            <h4 className="text-sm font-semibold text-foreground mb-2">Learning Outcomes</h4>
            <ul className="space-y-1.5 text-sm text-muted-foreground">
              <li>Design ML pipelines</li>
              <li>Evaluate model performance</li>
              <li>Implement deep learning models</li>
            </ul>
          </div>
        </div>
      </TabsContent>

      <TabsContent value="weekly-modules" className="mt-5">
        <div className="rounded-lg border bg-card shadow-card divide-y">
          {weeklyModules.map((mod) => (
            <div
              key={mod.week}
              className={`flex items-center gap-4 px-5 py-4 transition-colors ${
                mod.status === "current" ? "bg-badge/30" : ""
              } ${mod.status === "locked" ? "opacity-50" : ""}`}
            >
              <div className="flex-shrink-0">
                {mod.status === "completed" ? (
                  <CheckCircle2 className="h-5 w-5 text-progress-bar" />
                ) : mod.status === "current" ? (
                  <Circle className="h-5 w-5 text-accent" />
                ) : (
                  <Lock className="h-4 w-4 text-muted-foreground" />
                )}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-foreground">
                  Week {mod.week}: {mod.title}
                </p>
                {mod.status === "current" && (
                  <p className="text-xs text-accent mt-0.5 font-medium">In Progress</p>
                )}
              </div>
            </div>
          ))}
        </div>
      </TabsContent>

      <TabsContent value="grading-policy" className="mt-5">
        <div className="rounded-lg border bg-card p-5 shadow-card space-y-4">
          <h3 className="text-base font-semibold text-foreground font-serif">Grading Breakdown</h3>
          <div className="space-y-3">
            {[
              { item: "Weekly Assignments", weight: "30%", desc: "8 assignments, best 6 counted" },
              { item: "Midterm Exam", weight: "20%", desc: "Take-home, open-book format" },
              { item: "Capstone Project", weight: "30%", desc: "Individual research project" },
              { item: "Final Exam", weight: "15%", desc: "Comprehensive assessment" },
              { item: "Participation", weight: "5%", desc: "Forum engagement and peer reviews" },
            ].map((g) => (
              <div key={g.item} className="flex items-start justify-between py-2 border-b last:border-0">
                <div>
                  <p className="text-sm font-medium text-foreground">{g.item}</p>
                  <p className="text-xs text-muted-foreground mt-0.5">{g.desc}</p>
                </div>
                <span className="text-sm font-semibold text-accent">{g.weight}</span>
              </div>
            ))}
          </div>
        </div>
      </TabsContent>

      <TabsContent value="certification" className="mt-5">
        <div className="rounded-lg border bg-card p-5 shadow-card space-y-4">
          <h3 className="text-base font-semibold text-foreground font-serif">Professional Certificate</h3>
          <p className="text-sm text-muted-foreground leading-relaxed">
            Upon successful completion with a grade of B or higher, you will receive a Professional Certificate 
            in Advanced Machine Learning, accredited by the university's continuing education division.
          </p>
          <div className="rounded-md bg-muted p-4">
            <h4 className="text-sm font-medium text-foreground mb-2">Requirements</h4>
            <ul className="space-y-1.5 text-sm text-muted-foreground">
              <li>Complete all weekly modules</li>
              <li>Submit capstone project</li>
              <li>Pass final exam with 70% or above</li>
              <li>Overall grade of B (80%) or higher</li>
            </ul>
          </div>
        </div>
      </TabsContent>
    </Tabs>
  );
};

export default CourseTabs;
