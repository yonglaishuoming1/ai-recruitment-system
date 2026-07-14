import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export function CandidatesPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">候选人管理</h2>
        <p className="text-muted-foreground">查看和管理所有候选人信息</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>候选人列表</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            候选人列表功能开发中，敬请期待...
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
