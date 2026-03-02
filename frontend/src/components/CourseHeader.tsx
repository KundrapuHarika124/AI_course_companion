import { BookOpen, Clock, User, Award } from "lucide-react";

const CourseHeader = () => {
  return (
    <div className="space-y-5">
      <div className="flex items-start justify-between">
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center gap-1.5 rounded-md bg-badge px-2.5 py-1 text-xs font-medium text-badge-foreground">
              <BookOpen className="h-3 w-3" />
              Graduate Level
            </span>
            <span className="inline-flex items-center gap-1.5 rounded-md bg-badge px-2.5 py-1 text-xs font-medium text-badge-foreground">
              <Clock className="h-3 w-3" />
              12 Weeks
            </span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground font-serif">
            Advanced Machine Learning
          </h1>
          <div className="flex items-center gap-4 text-sm text-muted-foreground">
            <span className="flex items-center gap-1.5">
              <User className="h-3.5 w-3.5" />
              Dr. Sarah Chen
            </span>
            <span className="flex items-center gap-1.5">
              <Award className="h-3.5 w-3.5" />
              Professional Certificate
            </span>
          </div>
        </div>
      </div>

      {/* Progress bar */}
      <div className="space-y-2">
        <div className="flex items-center justify-between text-sm">
          <span className="font-medium text-foreground">Course Progress</span>
          <span className="text-muted-foreground">Week 4 of 12 — 33%</span>
        </div>
        <div className="h-2 w-full rounded-full bg-progress-track">
          <div
            className="h-2 rounded-full bg-progress-bar transition-all duration-500"
            style={{ width: "33%" }}
          />
        </div>
      </div>
    </div>
  );
};

export default CourseHeader;
