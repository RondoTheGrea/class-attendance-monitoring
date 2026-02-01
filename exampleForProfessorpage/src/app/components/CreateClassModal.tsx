import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/app/components/ui/dialog";
import { Button } from "@/app/components/ui/button";
import { Input } from "@/app/components/ui/input";
import { Label } from "@/app/components/ui/label";
import { Textarea } from "@/app/components/ui/textarea";
import { Info } from "lucide-react";

interface CreateClassModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onCreateClass: (classData: any) => void;
}

export function CreateClassModal({ open, onOpenChange, onCreateClass }: CreateClassModalProps) {
  const [subject, setSubject] = useState("");
  const [section, setSection] = useState("");
  const [room, setRoom] = useState("");
  const [description, setDescription] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!subject.trim()) {
      alert("Please enter a subject name.");
      return;
    }

    const classData = {
      id: Date.now().toString(),
      subject,
      section,
      room,
      description,
      schedules: [], // Empty schedules - will be added later
      announcements: [],
      attendance: [],
      createdAt: new Date().toISOString()
    };

    onCreateClass(classData);
    
    // Reset form
    setSubject("");
    setSection("");
    setRoom("");
    setDescription("");
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle className="text-2xl text-slate-900">Create New Class</DialogTitle>
          <DialogDescription className="text-slate-600">
            Add basic class information. You can configure schedules after creating the class.
          </DialogDescription>
        </DialogHeader>
        
        <form onSubmit={handleSubmit} className="space-y-6 mt-4">
          <div className="space-y-5">
            <div>
              <Label htmlFor="subject" className="text-slate-700 font-semibold">
                Subject Name *
              </Label>
              <Input
                id="subject"
                placeholder="e.g., Introduction to Computer Science"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                required
                className="mt-2 border-slate-300"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="section" className="text-slate-700 font-semibold">
                  Section
                </Label>
                <Input
                  id="section"
                  placeholder="e.g., A, B, 101"
                  value={section}
                  onChange={(e) => setSection(e.target.value)}
                  className="mt-2 border-slate-300"
                />
              </div>

              <div>
                <Label htmlFor="room" className="text-slate-700 font-semibold">
                  Room
                </Label>
                <Input
                  id="room"
                  placeholder="e.g., Room 301"
                  value={room}
                  onChange={(e) => setRoom(e.target.value)}
                  className="mt-2 border-slate-300"
                />
              </div>
            </div>

            <div>
              <Label htmlFor="description" className="text-slate-700 font-semibold">
                Description
              </Label>
              <Textarea
                id="description"
                placeholder="Brief description of the class..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={3}
                className="mt-2 border-slate-300"
              />
            </div>

            <div className="bg-blue-50 border border-blue-200 p-4 rounded-lg flex gap-3">
              <Info className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
              <p className="text-sm text-blue-800">
                You can add class schedules, post announcements, and manage attendance after creating the class.
              </p>
            </div>
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t">
            <Button 
              type="button" 
              variant="outline" 
              onClick={() => onOpenChange(false)}
            >
              Cancel
            </Button>
            <Button 
              type="submit"
              className="bg-blue-600 hover:bg-blue-700"
            >
              Create Class
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
