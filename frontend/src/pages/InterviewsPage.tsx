import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export function InterviewsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">面试安排</h2>
        <p className="text-muted-foreground">安排和管理面试日程</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>面试日历</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            面试安排功能开发中，敬请期待...
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
