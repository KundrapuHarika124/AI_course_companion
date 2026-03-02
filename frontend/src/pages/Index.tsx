import CourseHeader from "@/components/CourseHeader";
import CourseTabs from "@/components/CourseTabs";
import AIAssistantPanel from "@/components/AIAssistantPanel";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      {/* Top nav bar */}
      <header className="border-b bg-card">
        <div className="mx-auto flex h-14 max-w-screen-2xl items-center justify-between px-6">
          <div className="flex items-center gap-6">
            <span className="text-base font-semibold text-foreground tracking-tight">LearnHub</span>
            <nav className="hidden md:flex items-center gap-5 text-sm text-muted-foreground">
              <span className="text-foreground font-medium">My Courses</span>
              <span className="hover:text-foreground transition-colors cursor-pointer">Calendar</span>
              <span className="hover:text-foreground transition-colors cursor-pointer">Grades</span>
            </nav>
          </div>
          <div className="flex items-center gap-3">
            <div className="h-8 w-8 rounded-full bg-primary flex items-center justify-center text-xs font-medium text-primary-foreground">
              SC
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <div className="mx-auto max-w-screen-2xl px-6 py-6">
        <div className="flex flex-col lg:flex-row gap-6 min-h-[calc(100vh-5rem)]">
          {/* Left panel - Course Dashboard */}
          <div className="flex-1 lg:w-[70%] space-y-6">
            <CourseHeader />
            <CourseTabs />
          </div>

          {/* Right panel - AI Assistant */}
          <div className="lg:w-[30%] lg:min-w-[340px]">
            <div className="lg:sticky lg:top-6 h-[calc(100vh-7rem)]">
              <AIAssistantPanel />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
